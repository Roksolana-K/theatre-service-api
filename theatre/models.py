from django.core.validators import MinValueValidator
from django.db import models


class Actor(models.Model):
    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)

    class Meta:
        verbose_name = "Actor"
        verbose_name_plural = "Actors"
        ordering = ("first_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True, null=False, blank=False)

    class Meta:
        verbose_name = "Genre"
        verbose_name_plural = "Genres"
        ordering = ("name",)

    def __str__(self):
        return f"{self.name}"


class Play(models.Model):
    title = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField(max_length=256, blank=False, null=False)
    actor = models.ManyToManyField(Actor, related_name="plays")
    genre = models.ManyToManyField(Genre, related_name="plays")

    class Meta:
        verbose_name = "Play"
        verbose_name_plural = "Plays"
        ordering = ("title",)

    def __str__(self):
        return f"{self.title}"


class TheatreHall(models.Model):
    name = models.CharField(max_length=100, unique=True, blank=False, null=False)
    rows = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)
    seats_in_row = models.IntegerField(validators=[MinValueValidator(1)], null=False, blank=False)

    class Meta:
        verbose_name = "Theatre Hall"
        verbose_name_plural = "Theatre Halls"
        ordering = ("name",)

    @property
    def seating_capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name}"


class Performance(models.Model):
    play = models.ForeignKey(Play, related_name="performances", on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, related_name="performances", on_delete=models.CASCADE)
    show_time = models.DateTimeField(null=False, blank=False)

    class Meta:
        verbose_name = "Performance"
        verbose_name_plural = "Performances"
        ordering = ("show_time",)
        unique_together = ("theatre_hall", "show_time")

    def __str__(self):
        return f"{self.play} at {self.show_time}"
