from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ApplicantViewSet, SpecializationViewSet

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(r"applicants", ApplicantViewSet, basename="applicants")
router_v1.register(
    r"specializations", SpecializationViewSet, basename="specializations"
)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
