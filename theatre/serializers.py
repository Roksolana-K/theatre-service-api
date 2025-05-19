from rest_framework import serializers

from theatre.models import Actor, Genre, Performance, Play, TheatreHall


class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = ("id", "first_name", "last_name")


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class PlaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Play
        fields = ("id", "title")


class PlayListSerializer(PlaySerializer):
    actor = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="full_name"
    )
    genre = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = Play
        fields = ("id", "title", "genre", "actor")


class PlayDetailSerializer(PlaySerializer):
    actor = ActorSerializer(many=True, read_only=True)
    genre = GenreSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ("id", "title", "description", "genre", "actor")


class TheatreHallSerializer(serializers.ModelSerializer):
    class Meta:
        model = TheatreHall
        fields = ("id", "name", "rows", "seats_in_row", "seating_capacity")


class PerformanceListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ("id", "play", "show_time")


class PerformanceDetailSerializer(PerformanceListSerializer):
    play_title = serializers.CharField(source="play.title", read_only=True)
    theatre_hall_name = serializers.CharField(
        source="theatre_hall.name", read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.seating_capacity", read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = (
            "id",
            "play_title",
            "show_time",
            "theatre_hall_name",
            "theatre_hall_capacity",
            "tickets_available",
        )
