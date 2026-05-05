from django.test import TestCase
from django.urls import reverse


class PatientsViewsTests(TestCase):
    def test_patients_summary(self):
        response = self.client.get(reverse("patients:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())
