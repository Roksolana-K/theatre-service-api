from django.db.models import Count, F
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from theatre.models import Actor, Genre, Performance, Play, TheatreHall
from theatre.serializers import ActorSerializer, GenreSerializer, PerformanceDetailSerializer, \
    PerformanceListSerializer, PlayDetailSerializer, \
    PlayListSerializer, \
    PlaySerializer, \
    TheatreHallSerializer


class TheatrePermissionMixin(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


class ActorViewSet(TheatrePermissionMixin):
    queryset = Actor.objects.all().order_by("first_name")
    serializer_class = ActorSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ("first_name", "last_name")
    ordering_fields = ("first_name","last_name")


class GenreViewSet(TheatrePermissionMixin):
    queryset = Genre.objects.all().order_by("name")
    serializer_class = GenreSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ("name",)


class PlayViewSet(TheatrePermissionMixin):
    queryset = Play.objects.all().prefetch_related("actor", "genre").order_by("title")
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("title", "actor__first_name", "actor__last_name", "genre__name")
    ordering_fields = ("title", "actor__first_name", "genre__name")


    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer
        elif self.action == "retrieve":
            return PlayDetailSerializer
        return PlaySerializer


class TheatreHallViewSet(TheatrePermissionMixin):
    queryset = TheatreHall.objects.all().order_by("name")
    serializer_class = TheatreHallSerializer
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ("name",)
    ordering_fields = ("name",)


class PerformanceViewSet(TheatrePermissionMixin):
    queryset = Performance.objects.all().select_related("theatre_hall", "play").annotate(tickets_available=(
        F("theatre_hall__rows") * F("theatre_hall__seats_in_row") - Count("tickets"))).order_by("show_time")
    serializer_class = PerformanceListSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PerformanceDetailSerializer
        return PerformanceListSerializer
