from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class UsersViewsTests(TestCase):
    def test_users_summary(self):
        response = self.client.get(reverse("users:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())

    def test_admin_can_access_manage(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="admin1",
            password="Test12345!",
            email="admin1@test.local",
            role="ADMIN",
            is_staff=True,
        )
        self.client.login(username="admin1", password="Test12345!")
        response = self.client.get(reverse("users:manage_list"))
        self.assertEqual(response.status_code, 200)
