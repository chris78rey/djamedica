from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Djamedica")

    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "ok", "app": "djamedica", "framework": "django"},
        )

    def test_dashboard_endpoint(self):
        response = self.client.get(reverse("dashboard"))
        self.assertEqual(response.status_code, 200)
        payload = response.json()
        self.assertIn("users", payload)
        self.assertIn("patients", payload)
        self.assertIn("doctors", payload)
        self.assertIn("specialties", payload)
        self.assertIn("appointments", payload)
