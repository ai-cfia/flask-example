import unittest
from app import app

class TestRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('keys/client_public_key.pem', 'rb') as f:
            cls.public_key = f.read().decode('utf-8')

    def setUp(self):
        self.client = app.test_client()

    def test_health_route(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b"ok")

    def test_hello_world_authenticated(self):
        #TODO
        pass

    def test_hello_world_no_token(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 302)

    def test_hello_world_valid_token(self):
        #TODO
        pass

    def test_hello_world_invalid_token(self):
        invalid_token = 'invalid_token_here'
        response = self.client.get(f"/?token={invalid_token}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('utf-8'), 'Invalid Token!')


if __name__ == "__main__":
    unittest.main()
