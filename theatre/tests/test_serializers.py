from django.db.models import Count, ExpressionWrapper, F, IntegerField
from django.test import TestCase
from datetime import timedelta
from django.utils import timezone

from theatre.models import Actor, Genre, Play, TheatreHall, Performance
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    TheatreHallSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
)


class SerializerTestCase(TestCase):
    def setUp(self):
        self.actor = Actor.objects.create(first_name="John", last_name="Doe")
        self.genre = Genre.objects.create(name="Comedy")
        self.play = Play.objects.create(title="Hamlet", description="Classic tragedy")
        self.play.actor.add(self.actor)
        self.play.genre.add(self.genre)

        self.hall = TheatreHall.objects.create(name="Big Hall", rows=5, seats_in_row=10)
        self.performance = Performance.objects.create(
            play=self.play,
            theatre_hall=self.hall,
            show_time=timezone.now() + timedelta(days=1)
        )

    def test_actor_serializer_output(self):
        serializer = ActorSerializer(self.actor)
        expected = {
            "id": self.actor.id,
            "first_name": "John",
            "last_name": "Doe"
        }
        self.assertEqual(serializer.data, expected)

    def test_genre_serializer_output(self):
        serializer = GenreSerializer(self.genre)
        expected = {
            "id": self.genre.id,
            "name": "Comedy"
        }
        self.assertEqual(serializer.data, expected)

    def test_play_list_serializer(self):
        serializer = PlayListSerializer(self.play)
        self.assertEqual(serializer.data["title"], "Hamlet")
        self.assertIn("Comedy", serializer.data["genre"])
        self.assertIn("John Doe", serializer.data["actor"])  # Спрацює якщо в моделі є @property full_name

    def test_play_detail_serializer(self):
        serializer = PlayDetailSerializer(self.play)
        self.assertEqual(serializer.data["title"], "Hamlet")
        self.assertEqual(serializer.data["genre"][0]["name"], "Comedy")
        self.assertEqual(serializer.data["actor"][0]["first_name"], "John")

    def test_theatre_hall_serializer_output(self):
        serializer = TheatreHallSerializer(self.hall)
        self.assertEqual(serializer.data["name"], "Big Hall")
        self.assertEqual(serializer.data["rows"], 5)
        self.assertEqual(serializer.data["seats_in_row"], 10)
        self.assertEqual(serializer.data["seating_capacity"], 50)  # 5 * 10

    def test_performance_list_serializer(self):
        serializer = PerformanceListSerializer(self.performance)
        self.assertEqual(serializer.data["play"], self.play.id)
        self.assertIn("show_time", serializer.data)

    def test_performance_detail_serializer(self):
        performance = Performance.objects.annotate(
            tickets_available=ExpressionWrapper(
                F("theatre_hall__rows") * F("theatre_hall__seats_in_row") - Count("tickets"),
                output_field=IntegerField()
            )
        ).get(id=self.performance.id)

        serializer = PerformanceDetailSerializer(performance)
        self.assertEqual(serializer.data["play_title"], "Hamlet")
        self.assertEqual(serializer.data["theatre_hall_name"], "Big Hall")
        self.assertEqual(serializer.data["theatre_hall_capacity"], 50)
        self.assertEqual(serializer.data["tickets_available"], 50)
