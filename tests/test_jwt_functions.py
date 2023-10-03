import unittest
from app import decode_jwt_token
from datetime import datetime, timedelta
import jwt

class TestDecodeJWT(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        with open('keys/client_public_key.pem', 'rb') as f:
            cls.public_key = f.read().decode('utf-8')

    def test_decode_valid_jwt(self):
        with open('keys/client_private_key.pem', 'rb') as f:
            private_key = f.read().decode('utf-8')
        data = {'user': 'testuser'}
        expiration_seconds=300
        expiration_time = datetime.utcnow() + timedelta(seconds=expiration_seconds)
        expiration_timestamp = int(expiration_time.timestamp())
        data['exp'] = expiration_timestamp
        token = jwt.encode(data, private_key, algorithm='RS256')
        unverified_header = jwt.get_unverified_header(token)
        self.assertEqual(unverified_header['alg'], 'RS256')
        decoded_data = decode_jwt_token(token, self.public_key)
        self.assertEqual(decoded_data['user'], 'testuser')
        self.assertEqual(decoded_data['exp'], expiration_timestamp)

    def test_decode_invalid_jwt(self):
        invalid_token = "invalid.token.here"
        token = decode_jwt_token(invalid_token, self.public_key)
        assert not token, f"expected token to be None, but it was {token}"

if __name__ == '__main__':
    unittest.main()
