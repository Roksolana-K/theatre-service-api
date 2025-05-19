from django.core.validators import MinValueValidator
from django.db import models
from theatre.models import Performance
from user.models import User


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ("created_at",)

    def __str__(self):
        return f"Reservation #{self.id} (Created at: {self.created_at})"


class Ticket(models.Model):
    row = models.IntegerField(
        validators=[MinValueValidator(1)], null=False, blank=False
    )
    seat = models.IntegerField(
        validators=[MinValueValidator(1)], null=False, blank=False
    )
    performance = models.ForeignKey(
        Performance, on_delete=models.CASCADE, related_name="tickets"
    )
    reservation = models.ForeignKey(
        Reservation, on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"
        unique_together = ("row", "seat", "performance")

    def __str__(self):
        return f"Ticket for: {self.performance.play.title}, seat: {self.seat}, row: {self.row}"
