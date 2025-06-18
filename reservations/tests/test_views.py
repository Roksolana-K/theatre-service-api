from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from reservations.models import Reservation, Ticket
from theatre.models import Performance, Play, TheatreHall

from django.utils import timezone
from datetime import timedelta


User = get_user_model()


class ReservationViewsTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="user@example.com", password="testpass123"
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
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
        self.ticket = Ticket.objects.create(
            reservation=self.reservation, performance=self.performance, row=1, seat=1
        )

    def test_create_reservation(self):
        self.client.force_authenticate(user=self.user)

        payload = {
            "tickets": [{"row": 2, "seat": 5, "performance": self.performance.id}]
        }

        url = reverse("reservations:create_reservation")
        response = self.client.post(url, data=payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)

    def test_list_reservations(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reservations:my_reservations")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_reservation_detail(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reservations:my_reservations")
        response = self.client.get(f"{url}{self.reservation.id}/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.reservation.id)

    def test_delete_reservation(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("reservations:my_reservations")
        response = self.client.delete(f"{url}{self.reservation.id}/delete/")

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Reservation.objects.filter(id=self.reservation.id).exists())

    def test_unauthenticated_access(self):
        url = reverse("reservations:my_reservations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_permissions_for_admin_view(self):
        # Unauthenticated user
        url = reverse("reservations:all_reservations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Regular user
        self.client.force_authenticate(user=self.user)
        url = reverse("reservations:all_reservations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Admin user
        self.client.force_authenticate(user=self.admin)
        url = reverse("reservations:all_reservations")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
