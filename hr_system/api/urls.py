from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from api.views import ApplicantsViewSet, SpecializationViewSet, VacancyViewSet

app_name = "api"

schema_view = get_schema_view(
    openapi.Info(
        title="HR-SYSTEM API",
        default_version="v1",
        description="HR-SYSTEM API documentation",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router_v1 = DefaultRouter()

router_v1.register(r"applicants", ApplicantsViewSet)
router_v1.register(r"specializations", SpecializationViewSet)
router_v1.register(r"vacancies", VacancyViewSet)

urlpatterns = [
    path(
        "swagger<format>/",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path(
        r"auth/sign-in",
        jwt_views.TokenObtainPairView.as_view(),
        name="sign_in",
    ),
    path(
        r"auth/refresh-token",
        jwt_views.TokenRefreshView.as_view(),
        name="refresh_token",
    ),
    path("", include(router_v1.urls)),
]
