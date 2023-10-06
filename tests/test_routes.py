import unittest
from unittest.mock import patch

from app import app


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.client = app.test_client()

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"ok")

    @patch("app.membrane_login_required")
    @patch("app.membrane_current_user")
    def test_example_endpoint_with_login(self, mock_current_user, mock_login_required):
        mock_current_user.id = "test_email@example.com"
        mock_login_required.side_effect = lambda func: func

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data.decode("utf-8"), "Hello, test_email@example.com!"
        )

    @patch("app.membrane_login_required")
    def test_example_endpoint_without_login(self, mock_login_required):
        mock_login_required.side_effect = lambda func: func

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello, world!")


if __name__ == "__main__":
    unittest.main()
