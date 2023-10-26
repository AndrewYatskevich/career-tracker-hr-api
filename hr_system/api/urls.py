from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import ApplicantsViewSet

app_name = "api"

router_v1 = DefaultRouter()
router_v1.register(r"applicants", ApplicantsViewSet)

urlpatterns = [
    path("v1/", include(router_v1.urls)),
]
