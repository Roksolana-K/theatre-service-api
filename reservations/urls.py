from django.urls import path, include
from rest_framework import routers


app_name = "cinema"

router = routers.DefaultRouter()

urlpatterns = [path("", include(router.urls))]