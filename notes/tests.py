from django.test import TestCase


class HealthCheckTest(TestCase):
    def test_healthz_route(self) -> None:
        # If you have named your URL pattern, use reverse('healthz')
        # Otherwise, you can just hardcode the path like '/healthz/'
        response = self.client.get("/healthz/")
        self.assertEqual(response.status_code, 200)
        # Optionally, check response content if you return any specific data
        self.assertJSONEqual(response.content, {"status": "ok"})
