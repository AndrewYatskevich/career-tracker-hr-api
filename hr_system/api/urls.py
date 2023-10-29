from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from api.views import ApplicantsViewSet, VacancyViewSet

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(r"applicants", ApplicantsViewSet)
router_v1.register(r"vacancies", VacancyViewSet)

urlpatterns = [
    path(
        r"v1/auth/sign-in",
        jwt_views.TokenObtainPairView.as_view(),
        name="sign_in",
    ),
    path(
        r"v1/auth/refresh-token",
        jwt_views.TokenRefreshView.as_view(),
        name="refresh_token",
    ),
    path("v1/", include(router_v1.urls)),
]
