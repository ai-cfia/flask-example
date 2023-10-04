import unittest
from datetime import datetime, timedelta

import jwt

from app import JWTDecodingError, decode_jwt_token, generate_jwt_token


class TestDecodeJWT(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open("tests/test_keys/public_key.pem", "rb") as f:
            cls.public_key = f.read()
        with open("tests/test_keys/private_key.pem", "rb") as f:
            cls.private_key = f.read()

    def test_encode_decode_valid_jwt(self):
        data = {"user": "testuser"}
        algorithm = "RS256"
        app_id = "test_app"
        expiration_seconds = 300
        headers = {
            "alg": algorithm,
            "app_id": app_id,
            "typ": "JWT",
            "field1": "value1",
            "field2": "value2",
        }
        expiration = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        timestamp = int(expiration.timestamp())
        token = generate_jwt_token(
            data, self.private_key, expiration_seconds, algorithm, app_id, headers
        )
        unverified_header = jwt.get_unverified_header(token)
        self.assertDictEqual(unverified_header, headers)
        decoded_data = decode_jwt_token(token, self.public_key)
        self.assertEqual(decoded_data["user"], "testuser")
        self.assertLessEqual(decoded_data["exp"], timestamp + 1)

    def test_decode_invalid_jwt(self):
        invalid_token = "invalid.token.here"
        with self.assertRaises(JWTDecodingError):
            decode_jwt_token(invalid_token, self.public_key)


if __name__ == "__main__":
    unittest.main()
