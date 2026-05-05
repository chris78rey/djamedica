from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class SpecialtiesViewsTests(TestCase):
    def test_specialties_summary(self):
        response = self.client.get(reverse("specialties:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())

    def test_admin_can_access_manage(self):
        User = get_user_model()
        admin_user = User.objects.create_user(
            username="adminspec",
            password="Test12345!",
            email="adminspec@test.local",
            role="ADMIN",
            is_staff=True,
        )
        self.client.login(username="adminspec", password="Test12345!")
        response = self.client.get(reverse("specialties:manage_list"))
        self.assertEqual(response.status_code, 200)
