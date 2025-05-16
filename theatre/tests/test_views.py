from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.test import TestCase
from user.models import User
from theatre.models import Actor, Genre, Play, TheatreHall, Performance
from datetime import timedelta
from django.utils import timezone


class TheatreViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(email="user@example.com", password="testpass123")
        self.admin = User.objects.create_superuser(email="admin@example.com", password="adminpass123")

        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Tragedy")
        self.hall = TheatreHall.objects.create(name="Big Hall", rows=10, seats_in_row=20)
        self.play = Play.objects.create(title="Hamlet")
        self.play.genre.add(self.genre)
        self.play.actor.add(self.actor)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timedelta(days=1)
        )

    def test_actor_list_view_anonymous(self):
        url = reverse("theatre:actor-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actor_detail_view_anonymous(self):
        url = reverse("theatre:actor-detail", args=[self.actor.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_actor_create_forbidden_for_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("theatre:actor-list")
        data = {"first_name": "Test", "last_name": "User"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_actor_create_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("theatre:actor-list")
        data = {"first_name": "Test", "last_name": "Admin"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_list_view_anonymous(self):
        url = reverse("theatre:genre-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_genre_detail_view_anonymous(self):
        url = reverse("theatre:genre-detail", args=[self.genre.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_play_list_view_anonymous(self):
        url = reverse("theatre:play-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_play_detail_view_anonymous(self):
        url = reverse("theatre:play-detail", args=[self.play.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_play_create_forbidden_for_user(self):
        self.client.force_authenticate(self.user)
        url = reverse("theatre:play-list")
        data = {"title": "Test Play", "genre": [self.genre.id], "actor": [self.actor.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_play_create_allowed_for_admin(self):
        self.client.force_authenticate(self.admin)
        url = reverse("theatre:play-list")
        data = {"title": "Test Play", "genre": [self.genre.id], "actor": [self.actor.id]}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_theatre_hall_list_view_anonymous(self):
        url = reverse("theatre:theatrehall-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_theatre_hall_detail_view_anonymous(self):
        url = reverse("theatre:theatrehall-detail", args=[self.hall.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performance_list_view_anonymous(self):
        url = reverse("theatre:performance-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_performance_detail_view_anonymous(self):
        url = reverse("theatre:performance-detail", args=[self.performance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
