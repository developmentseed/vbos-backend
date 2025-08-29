from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from .users.views import UserViewSet

API_BASE_URL = "api/v1"

api_urls = [
    path(
        f"{API_BASE_URL}/",
        include(("vbos.users.urls", "vbos.users"), namespace="users"),
    ),
    path(
        f"{API_BASE_URL}/",
        include(("vbos.datasets.urls", "vbos.datasets"), namespace="datasets"),
    ),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(api_urls)),
    path("api-token-auth/", views.obtain_auth_token),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # API-Docs
    path(f"{API_BASE_URL}/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        f"{API_BASE_URL}/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
