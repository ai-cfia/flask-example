import unittest

from app import JWTDecodingError, app, decode_jwt_token


class TestRoutes(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("tests/test_keys/public_key.pem", "rb") as f:
            cls.public_key = f.read()

    def setUp(self):
        self.client = app.test_client()

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"ok")

    def test_hello_world_authenticated(self):
        # TODO
        pass

    def test_hello_world_no_token(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_hello_world_valid_token(self):
        # TODO
        pass

    def test_hello_world_invalid_token(self):
        invalid_token = "invalid_token_here"
        with self.assertRaises(JWTDecodingError):
            decode_jwt_token(invalid_token, self.public_key)


if __name__ == "__main__":
    unittest.main()
