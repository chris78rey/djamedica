from django.test import TestCase
from django.urls import reverse


class UsersViewsTests(TestCase):
    def test_users_summary(self):
        response = self.client.get(reverse("users:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())
