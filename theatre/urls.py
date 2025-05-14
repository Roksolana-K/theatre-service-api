from django.urls import path, include
from rest_framework import routers


app_name = "cinema"

router = routers.DefaultRouter()
router.register()

urlpatterns = [path("", include(router.urls))]
