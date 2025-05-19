from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


User = get_user_model()

REGISTER_URL = reverse("user:register")
MANAGE_URL = reverse("user:my_info")
DELETE_URL = reverse("user:my_info_delete")
LIST_URL = reverse("user:all_users")


def create_user(**params):
    return User.objects.create_user(**params)


def get_token(client, email, password):
    url = reverse("token_obtain_pair")
    res = client.post(url, {"email": email, "password": password})
    return res.data["access"]


class UserViewTests(APITestCase):
    def setUp(self):
        self.user = create_user(
            email="user@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
        )
        self.admin = User.objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )

    def test_create_user_success(self):
        payload = {
            "email": "new@example.com",
            "password": "newpass123",
            "password2": "newpass123",
        }
        res = self.client.post(REGISTER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", res.data)
        self.assertNotIn("password", res.data)

    def test_create_user_invalid_password(self):
        payload = {
            "email": "new@example.com",
            "password": "newpass123",
            "password2": "newpass125",  # Паролі не однакові
        }
        res = self.client.post(REGISTER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("non_field_errors", res.data)
        self.assertIn("Passwords don't match", str(res.data["non_field_errors"]))

    def test_manage_user_retrieve(self):
        token = get_token(self.client, "user@example.com", "testpass123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)

    def test_manage_user_update(self):
        token = get_token(self.client, "user@example.com", "testpass123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        payload = {"first_name": "Updated", "last_name": "Name"}
        res = self.client.patch(MANAGE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Updated")

    def test_manage_user_requires_auth(self):
        res = self.client.get(MANAGE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_user_success(self):
        token = get_token(self.client, "user@example.com", "testpass123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.delete(DELETE_URL)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(User.objects.filter(email="user@example.com").exists())

    def test_list_users_admin_only(self):
        token = get_token(self.client, "admin@example.com", "adminpass123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.get(LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(len(res.data) >= 1)

    def test_list_users_forbidden_for_normal_user(self):
        token = get_token(self.client, "user@example.com", "testpass123")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
        res = self.client.get(LIST_URL)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
