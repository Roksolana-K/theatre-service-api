from django.contrib import admin
from reservations.models import Reservation


@admin.register(Reservation)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("user", "created_at")
    search_fields = ("created_at",)
