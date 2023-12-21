import unittest

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import asymmetric, serialization
from flask_login import login_user
from membrane.client.flask import User

from config import Config
from app_creator import create_app


def generate_key_pair():
    private_key = asymmetric.rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption(),
    )

    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    return private_pem.decode("utf-8"), public_pem.decode("utf-8")


class ConfigWithMembrane(Config):
    """Custom config with Membrane activated for tests."""

    MEMBRANE_SERVER = "http://test_server"
    SECRET_KEY = "test"
    ALGORITHM = "RS256"
    CLIENT_PRIVATE_KEY, SERVER_PUBLIC_KEY = generate_key_pair()
    PERMANENT_SESSION_LIFETIME = 300
    TOKEN_EXPIRES_IN_SECONDS = 300
    APP_ID = "test_app"
    REDIRECT_PATH = "/"


class ConfigWithoutMembrane(Config):
    """Custom config without Membrane activated for tests."""

    MEMBRANE_SERVER = None
    SECRET_KEY = None
    ALGORITHM = None
    CLIENT_PRIVATE_KEY = None
    SERVER_PUBLIC_KEY = None
    PERMANENT_SESSION_LIFETIME = None
    TOKEN_EXPIRES_IN_SECONDS = None
    APP_ID = None
    REDIRECT_PATH = None


class TestRoutesWithMembrane(unittest.TestCase):
    def setUp(self):
        self.config = ConfigWithMembrane()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_health_route(self):
        """Test that /health route returns 'ok' and a 200 status code."""
        with self.app.test_request_context():
            response = self.client.get("/health")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b"ok")

    def test_example_endpoint_with_login(self):
        """Test that the / route returns 200 when a user is logged in."""
        with self.app.test_request_context():
            test_user = User("user@example.com")
            login_user(test_user)
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)

    def test_example_endpoint_with_login_redirect(self):
        """Test that the / route redirects when a user is not logged in."""
        with self.app.test_request_context():
            response = self.client.get("/")
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                response.headers["Location"].startswith(self.config.MEMBRANE_SERVER)
            )

    def test_logout(self):
        """Test that the logout route redirects to root with no cookie."""
        with self.app.test_request_context():
            test_user = User("user@example.com")
            login_user(test_user)
            response = self.client.get("/logout", follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                response.headers["Location"].endswith(self.config.REDIRECT_PATH)
            )

    def test_login_when_user_not_logged_in(self):
        """Test that the login route redirects to membrane when no user is logged in."""
        with self.app.test_request_context():
            response = self.client.get("/login", follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                response.headers["Location"].startswith(self.config.MEMBRANE_SERVER)
            )

    def test_login_when_user_logged_in(self):
        """Test that the login route redirects to root when a user is logged in."""
        with self.app.test_request_context():
            test_user = User("user@example.com")
            login_user(test_user)
            response = self.client.get("/login", follow_redirects=False)
            self.assertEqual(response.status_code, 302)
            self.assertTrue(
                response.headers["Location"].endswith(self.config.REDIRECT_PATH)
            )


class TestRoutesWithoutMembrane(unittest.TestCase):
    def setUp(self):
        self.config = ConfigWithoutMembrane()
        self.app = create_app(self.config)
        self.client = self.app.test_client()

    def test_example_endpoint_without_login(self):
        """Test that the / route returns 200 when membrane is disabled."""
        with self.app.test_request_context():
            response = self.client.get("/")
            self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
