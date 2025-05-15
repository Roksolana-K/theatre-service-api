from django.urls import path, include
from rest_framework import routers

from theatre.views import ActorViewSet, GenreViewSet, PerformanceViewSet, PlayViewSet, TheatreHallViewSet

app_name = "cinema"

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("plays", PlayViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("performances", PerformanceViewSet)


urlpatterns = [
    path("", include(router.urls))

]
