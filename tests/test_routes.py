import unittest

from app import app
from unittest import IsolatedAsyncioTestCase

class TestQuartRoutes(IsolatedAsyncioTestCase):

    @classmethod
    def setUpClass(cls):
        with open('keys/client_public_key.pem', 'rb') as f:
            cls.public_key = f.read().decode('utf-8')

    def setUp(self):
        self.client = app.test_client()

    async def test_health_route(self):
        response = await self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(await response.get_data(), b"ok")

    async def test_hello_world_authenticated(self):
        #TODO
        pass

    async def test_hello_world_no_token(self):
        response = await self.client.get("/")
        self.assertEqual(response.status_code, 302) 

    async def test_hello_world_valid_token(self):
        #TODO
        pass

    async def test_hello_world_invalid_token(self):
        invalid_token = 'invalid_token_here'
        response = await self.client.get(f"/?token={invalid_token}")
        self.assertEqual(response.status_code, 200) 
        self.assertEqual(await response.get_data(as_text=True), 'Invalid Token!')


if __name__ == "__main__":
    unittest.main()
