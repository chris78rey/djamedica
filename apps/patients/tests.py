from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class PatientsViewsTests(TestCase):
    def test_patients_summary(self):
        response = self.client.get(reverse("patients:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())

    def test_manage_requires_login(self):
        response = self.client.get(reverse("patients:manage_list"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_access_manage(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="staff1",
            password="Test12345!",
            email="staff1@test.local",
            role="STAFF",
        )
        self.client.login(username="staff1", password="Test12345!")
        response = self.client.get(reverse("patients:manage_list"))
        self.assertEqual(response.status_code, 200)
