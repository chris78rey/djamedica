from django.test import TestCase
from django.urls import reverse


class AppointmentsViewsTests(TestCase):
    def test_appointments_summary(self):
        response = self.client.get(reverse("appointments:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())
