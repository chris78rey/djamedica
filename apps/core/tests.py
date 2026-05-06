from django.contrib.auth import get_user_model
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
            {"status": "ok", "app": "djamedica", "framework": "django", "database": "ok"},
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

    def test_panel_requires_login(self):
        response = self.client.get(reverse("panel"))
        self.assertEqual(response.status_code, 302)

    def test_panel_logged_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username="staffpanel",
            password="Test12345!",
            email="staffpanel@test.local",
            role="STAFF",
        )
        self.client.login(username="staffpanel", password="Test12345!")
        response = self.client.get(reverse("panel"))
        self.assertEqual(response.status_code, 200)
