from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

urlpatterns = [
    path("api/v1/", include("api.urls", namespace="api_v1")),
    path("admin/", admin.site.urls),
]

urlpatterns += staticfiles_urlpatterns()
