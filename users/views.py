from rest_framework import generics, permissions,status
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
import random
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializers import RegisterSerializer, UserSerializer, VerifySerializer, LoginSerializer, ResendCodeSerializer
from .permissions import IsAdminRole
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from .tasks import send_verification_email
from rest_framework.pagination import PageNumberPagination
from django.core.cache import cache

class RegisterView(generics.CreateAPIView):
    """
    summary: Sign up
    description: Create a new user with 'unverified' status.
    Generates a 6-digit verification code (valid for 1 hour)
    and sends it via email using SMTP (async via Celery).
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save(is_verified=False)
        code = f"{random.randint(100000, 999999)}"
        user.verification_code = code
        user.verification_expires_at = timezone.now() + timedelta(hours=1)
        user.save()

        send_verification_email.delay(user.email, code)

        self.verification_response = {
            "message": "User registered successfully. Verification code sent to your email.",
            "email": user.email,
            "expires_at": user.verification_expires_at,
        }

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = getattr(self, "verification_response", response.data)
        return response


class VerifyView(APIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = VerifySerializer

    @swagger_auto_schema(
        operation_summary="Verify account",
        operation_description="Confirm verification by providing `email` and 6-digit `code`.",
        request_body=VerifySerializer,
        responses={
            200: openapi.Response(description="Verification successful"),
            400: openapi.Response(description="Invalid or expired code"),
            404: openapi.Response(description="User not found"),
        },
    )
    def post(self, request):
        serializer = VerifySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.verification_code != code or timezone.now() > user.verification_expires_at:
            return Response({"detail": "Invalid or expired code"}, status=status.HTTP_400_BAD_REQUEST)

        user.is_verified = True
        user.verification_code = None
        user.verification_expires_at = None
        user.save()

        return Response({"detail": "Verification successful"}, status=status.HTTP_200_OK)


class ResendVerificationCodeView(generics.GenericAPIView):
    serializer_class = ResendCodeSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Resend verification code",
        operation_description="Resend verification code via email if not verified yet.",
        request_body=ResendCodeSerializer,
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if user.is_verified:
            return Response({"detail": "User already verified"}, status=status.HTTP_400_BAD_REQUEST)

        code = f"{random.randint(100000, 999999)}"
        user.verification_code = code
        user.verification_expires_at = timezone.now() + timedelta(hours=1)
        user.save()

        send_verification_email.delay(user.email, code)

        return Response({
            "message": "New verification code sent to your email.",
            "email": user.email,
            "expires_at": user.verification_expires_at
        }, status=status.HTTP_200_OK)



class LoginView(generics.GenericAPIView):
    """
    summary: Login
    description: Authenticate user and issue JWT tokens (access & refresh).
    Only verified users can log in.
    """
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_summary="Login user",
        operation_description=(
            "Provide email and password to get JWT access and refresh tokens. "
            "Note: Only verified users can log in."
        ),
        request_body=LoginSerializer,
        responses={
            200: openapi.Response(description="Login successful"),
            400: openapi.Response(description="User not verified"),
            401: openapi.Response(description="Invalid credentials"),
        },
    )
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        # 🔒 Verify check
        if not user.is_verified:
            return Response(
                {"detail": "Email not verified. Please verify your account before logging in."},
                status=status.HTTP_400_BAD_REQUEST
            )

        refresh = RefreshToken.for_user(user)
        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh)
        })


class MeView(generics.RetrieveAPIView):
    # summary: Get current user
    # description: Return the authenticated user's profile.
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

class UserPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' 
    max_page_size = 100


class UserListView(generics.ListAPIView):
    """
    List all users with Redis caching and pagination.
    Cache is automatically cleared when users are added, updated, or deleted.
    """
    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
    pagination_class = UserPagination

    def get_queryset(self):
        cache_key = "cached_users"
        users = cache.get(cache_key)

        if not users:
            print("🧠 Fetching from database...")
            users = list(User.objects.all().order_by("id"))
            cache.set(cache_key, users, timeout=60 * 5)  # Cache for 5 minutes
        else:
            print("⚡ Loaded from Redis cache!")

        return users
    

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    # summary: Get/Update/Delete user by ID
    # description: Admin-only. Partial updates allowed.
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRole]
