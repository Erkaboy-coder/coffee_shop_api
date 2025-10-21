from django.urls import path
from .views import RegisterView, VerifyView, LoginView, MeView, UserListView, UserDetailView, ResendVerificationCodeView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/signup/", RegisterView.as_view(), name="auth-signup"),
    path("auth/login/", LoginView.as_view(), name="auth-login"),
    path("auth/verify/", VerifyView.as_view(), name="auth-verify"),
    path("auth/resend-code/", ResendVerificationCodeView.as_view(), name="resend-code"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="auth-refresh"),
    path("me/", MeView.as_view(), name="me"),
    path("users/", UserListView.as_view(), name="users-list"),
    path("users/<int:pk>/", UserDetailView.as_view(), name="users-detail"),
]
