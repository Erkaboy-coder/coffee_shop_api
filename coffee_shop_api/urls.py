from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
from django.conf.urls.static import static

# 🔹 Swagger konfiguratsiyasi
schema_view = get_schema_view(
    openapi.Info(
        title="☕ Coffee Shop API",
        default_version="v1",
        description=(
            "Coffee Shop API — user registration, login, JWT authentication, "
            "and email verification module."
        ),
        contact=openapi.Contact(email="support@coffeeshop.local"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# 🔹 Asosiy URL konfiguratsiya
urlpatterns = [
    path("admin/", admin.site.urls),

    # API moduli
    path("api/", include("users.urls")),

    # Swagger UI
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # Root sahifada ham Swagger chiqadi
    path("", schema_view.with_ui("swagger", cache_timeout=0), name="root-swagger"),
]

# 🔹 Static va media fayllar (faqat DEBUG=True bo‘lsa)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
