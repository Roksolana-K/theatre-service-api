from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from reservations.models import Reservation, Ticket
from theatre.models import Performance, Play, TheatreHall

from reservations.serializers import (
    TicketSerializer,
    ReservationSerializer,
)

User = get_user_model()

class SerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.play = Play.objects.create(title="Hamlet")
        self.hall = TheatreHall.objects.create(
            name="Main Hall", rows=10, seats_in_row=10
        )
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timedelta(days=1),
        )
        self.reservation = Reservation.objects.create(user=self.user)

    def test_ticket_serializer_valid(self):
        payload = {"row": 3, "seat": 4, "performance": self.performance.id}
        serializer = TicketSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_ticket_serializer_invalid_duplicate_seat(self):
        Ticket.objects.create(
            row=5, seat=6, performance=self.performance, reservation=self.reservation
        )

        payload = {"row": 5, "seat": 6, "performance": self.performance.id}
        serializer = TicketSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)

    def test_ticket_serializer_missing_performance(self):
        payload = {"row": 1, "seat": 1}
        serializer = TicketSerializer(data=payload)
        self.assertFalse(serializer.is_valid())
        self.assertIn("performance", serializer.errors)

    def test_reservation_serializer_creates_reservation_with_tickets(self):
        payload = {
            "tickets": [
                {"row": 2, "seat": 5, "performance": self.performance.id},
                {"row": 2, "seat": 6, "performance": self.performance.id},
            ]
        }

        serializer = ReservationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        reservation = serializer.save(user=self.user)

        self.assertEqual(
            Reservation.objects.count(), 2
        )  # one created in setUp + new one
        self.assertEqual(reservation.tickets.count(), 2)
