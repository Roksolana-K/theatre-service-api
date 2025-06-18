from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

from user.serializers import (
    UserCreateSerializer,
    UserUpdateSerializer,
    UserDetailSerializer,
    UserListSerializer,
)
from theatre.models import Genre

User = get_user_model()


class UserSerializerTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="strongpassword123",
            first_name="Test",
            last_name="User",
        )
        self.genre1 = Genre.objects.create(name="Drama")
        self.genre2 = Genre.objects.create(name="Comedy")

    # --- UserCreateSerializer ---

    def test_user_create_valid_data(self):
        data = {
            "email": "new@example.com",
            "password": "strongpass123",
            "password2": "strongpass123",
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertTrue(user.check_password(data["password"]))

    def test_user_create_password_mismatch(self):
        data = {
            "email": "new@example.com",
            "password": "strongpass123",
            "password2": "wrongpass",
        }
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("non_field_errors", serializer.errors)
        self.assertIn(
            "Passwords don't match", str(serializer.errors["non_field_errors"])
        )

    # --- UserUpdateSerializer ---

    def test_user_update_basic_fields(self):
        data = {
            "email": "updated@example.com",
            "first_name": "Updated",
            "last_name": "User",
            "favorite_genres": [self.genre1.name, self.genre2.name],
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertEqual(user.email, data["email"])
        self.assertEqual(user.first_name, data["first_name"])
        self.assertEqual(user.favorite_genres.count(), 2)

    def test_user_update_password(self):
        data = {
            "email": self.user.email,
            "password": "newstrongpass123",
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "favorite_genres": [],
        }
        serializer = UserUpdateSerializer(instance=self.user, data=data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()
        self.assertTrue(user.check_password("newstrongpass123"))

    # --- UserDetailSerializer ---

    def test_user_detail_serializer(self):
        self.user.favorite_genres.add(self.genre1)
        serializer = UserDetailSerializer(self.user)
        self.assertEqual(serializer.data["email"], self.user.email)
        self.assertIn(self.genre1.name, serializer.data["favorite_genres"])

    # --- UserListSerializer ---

    def test_user_list_serializer(self):
        serializer = UserListSerializer(self.user)
        self.assertEqual(serializer.data["email"], self.user.email)
        self.assertEqual(serializer.data["first_name"], self.user.first_name)
