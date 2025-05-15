from django.db import transaction
from rest_framework import serializers

from reservations.models import Reservation, Ticket
from theatre.models import Performance


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")

    def validate(self, data):
        performance = self.context.get("performance")
        if not performance:
            raise serializers.ValidationError("Performance not provided.")

        row = data["row"]
        seat = data["seat"]

        if Ticket.objects.filter(performance=performance, row=row, seat=seat).exists():
            raise serializers.ValidationError(f"Seat {seat} in row {row} is already taken.")
        return data


class TicketListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "performance", "row", "seat")


class TicketDetailSerializer(serializers.ModelSerializer):
    show_time = serializers.DateTimeField(source="performance.show_time", read_only=True)
    show_name = serializers.CharField(source="performance.play.title", read_only=True)
    theatre_hall = serializers.CharField(source="performance.theatre_hall.name", read_only=True)
    created_at = serializers.DateTimeField(source="reservation.created_at", read_only=True)

    class Meta:
        model = Ticket
        fields = ("id", "show_time", "show_name", "theatre_hall", "row", "seat", "created_at")


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets", "created_at")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if hasattr(self, "initial_data") and self.initial_data.get("performance"):
            performance_id = self.initial_data.get("performance")
            try:
                performance = Performance.objects.get(pk=performance_id)
                self.fields["tickets"].child.context.update({"performance": performance})
            except Performance.DoesNotExist:
                pass

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets")
            performance = validated_data["performance"]
            reservation = Reservation.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(reservation=reservation, performance=performance, **ticket_data)
            return reservation


class ReservationListSerializer(serializers.ModelSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ("id", "tickets")
