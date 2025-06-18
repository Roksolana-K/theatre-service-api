import debug_toolbar
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path(
        "admin/",
        admin.site.urls
    ),
    path(
        "api/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "__debug__/",
        include(debug_toolbar.urls)
    ),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema"
    ),
    path(
        "api/schema/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="schema-swagger",
    ),
    path(
        "api/schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="schema-redoc",
    ),
    path(
        "api/user/",
        include("user.urls",namespace="user")
    ),
    path(
        "api/theatre/",
        include("theatre.urls", namespace="theatre")
    ),
    path(
        "api/reservations/",
        include("reservations.urls", namespace="reservations")
    ),
]
