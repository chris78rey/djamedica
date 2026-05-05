from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AppointmentsViewsTests(TestCase):
    def test_appointments_summary(self):
        response = self.client.get(reverse("appointments:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())

    def test_staff_can_access_manage(self):
        User = get_user_model()
        staff_user = User.objects.create_user(
            username="staffappt",
            password="Test12345!",
            email="staffappt@test.local",
            role="STAFF",
        )
        self.client.login(username="staffappt", password="Test12345!")
        response = self.client.get(reverse("appointments:manage_list"))
        self.assertEqual(response.status_code, 200)
