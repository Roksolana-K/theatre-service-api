from rest_framework import filters, generics
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated

from reservations.models import Reservation
from reservations.serializers import ReservationListSerializer, ReservationSerializer, TicketSoldSeatsSerializer


class CreateReservationView(generics.CreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class MyReservationListView(generics.ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = filters.OrderingFilter
    ordering_fields = ("created_at",)

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-created_at")


class MyReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(
            user=self.request.user
        ).select_related("user").prefetch_related("tickets__performance__play")


class MyReservationDeleteView(generics.DestroyAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class AdminReservationListView(generics.ListAPIView):
    serializer_class = ReservationListSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        return Reservation.objects.all().prefetch_related(
            "tickets__performance__play", "user"
        ).order_by("-created_at")
