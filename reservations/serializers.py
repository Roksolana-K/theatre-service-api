from django.db import transaction
from rest_framework import serializers

from reservations.models import Reservation, Ticket


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat")


class TicketDetailSerializer(serializers.ModelSerializer):
    show_time = serializers.DateTimeField(source="performance.show_time", read_only=True)
    show_name = serializers.CharField(source="performance.play.title", read_only=True)
    theatre_hall = serializers.CharField(source="performance.theatre_hall.name", read_only=True)
    created_at = serializers.DateTimeField(source="reservation.created-at", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "show_time", "show_name", "theatre_hall", "row", "seat", "created_at")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketDetailSerializer(many=True, read_only=False, allow_empty=False)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, **ticket_data)
            return reservation


class ReservationListSerializer(ReservationSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
