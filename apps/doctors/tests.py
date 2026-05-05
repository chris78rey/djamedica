from django.test import TestCase
from django.urls import reverse


class DoctorsViewsTests(TestCase):
    def test_doctors_summary(self):
        response = self.client.get(reverse("doctors:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())
