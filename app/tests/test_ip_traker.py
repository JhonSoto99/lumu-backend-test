import unittest

from fastapi.testclient import TestClient
from ip_tracker.consumer import app


class TestAPI(unittest.TestCase):
    def setUp(self):
        """Initial setup for the tests."""
        self.client = TestClient(app)

    def test_get_unique_ip_count(self):
        """Test for the /api/v1/unique_ip_count endpoint."""
        response = self.client.get("/api/v1/unique_ip_count")
        self.assertEqual(response.status_code, 200)
        self.assertIn("unique_ip_count", response.json())


if __name__ == "__main__":
    unittest.main()
