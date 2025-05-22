from django.contrib import admin
from user.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "username", "phone_number")
    search_fields = ("first_name", "last_name", "username", "phone_number", "birth_date")
    list_filter = ("first_name", "birth_date", "favorite_genres")
