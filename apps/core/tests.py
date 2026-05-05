from django.test import TestCase
from django.urls import reverse


class CoreViewsTests(TestCase):
    def test_health_endpoint(self):
        response = self.client.get(reverse("health"))
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(
            response.content,
            {"status": "ok", "app": "djamedica", "framework": "django"},
        )

    def test_home_page(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Djamedica")
