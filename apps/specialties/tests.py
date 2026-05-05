from django.test import TestCase
from django.urls import reverse


class SpecialtiesViewsTests(TestCase):
    def test_specialties_summary(self):
        response = self.client.get(reverse("specialties:summary"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("total", response.json())
