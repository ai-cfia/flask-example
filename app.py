import os
from datetime import datetime, timedelta

import jwt
from dotenv import load_dotenv
from flask import Flask, redirect, request, session, url_for

load_dotenv()


# Custom exceptions
class JWTError(Exception):
    """Base class for JWT related exceptions."""


class JWTGenerationError(JWTError):
    """Exception raised for errors during JWT generation."""


class JWTDecodingError(JWTError):
    """Exception raised for errors during JWT decoding."""


# Constants
SECRET_KEY = os.getenv("FASTAPI_EXAMPLE_SECRET_KEY")
APP_ID = os.getenv("FASTAPI_EXAMPLE_APP_ID", "flask_example")
ALGORITHM = os.getenv("FASTAPI_EXAMPLE_ALGORITHM", "RS256")
SERVER_PUBLIC_KEY_FILE = os.getenv(
    "FASTAPI_EXAMPLE_SERVER_PUBLIC_KEY_FILE", "keys/server_public_key.pem"
)
CLIENT_PRIVATE_KEY_FILE = os.getenv(
    "FASTAPI_EXAMPLE_CLIENT_PRIVATE_KEY_FILE", "keys/client_private_key.pem"
)
SESSION_LIFETIME = int(os.getenv("FASTAPI_EXAMPLE_SESSION_LIFETIME", 300))
TOKEN_EXPIRES_IN_SECONDS = int(
    os.getenv("FASTAPI_EXAMPLE_TOKEN_EXPIRES_IN_SECONDS", 300)
)
MEMBRANE_SERVER = os.getenv("FASTAPI_EXAMPLE_MEMBRANE_SERVER", "http://127.0.0.1:5000")

# Read key files at startup
with open(SERVER_PUBLIC_KEY_FILE, "rb") as file:
    SERVER_PUBLIC_KEY = file.read()

with open(CLIENT_PRIVATE_KEY_FILE, "rb") as file:
    CLIENT_PRIVATE_KEY = file.read()


# Initialize Flask and configuration
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=SESSION_LIFETIME)


def generate_jwt_token(
    payload: dict[str, any],
    private_key: str,
    expires_in_seconds: int = TOKEN_EXPIRES_IN_SECONDS,
    algorithm: str = ALGORITHM,
    app_id: str = APP_ID,
    additional_headers: dict[str, any] | None = None,
) -> str:
    try:
        new_payload = payload.copy()
        if "exp" not in new_payload:
            expiration_time = datetime.utcnow() + timedelta(seconds=expires_in_seconds)
            new_payload["exp"] = int(expiration_time.timestamp())
        headers = {"alg": algorithm, "app_id": app_id, "typ": "JWT"}
        if additional_headers:
            headers.update(additional_headers)
        return jwt.encode(
            new_payload, private_key, algorithm=algorithm, headers=headers
        )
    except jwt.InvalidKeyError as e:
        raise JWTGenerationError(f"Invalid key: {e}") from e


def decode_jwt_token(
    jwt_token: str, public_key: str, algorithm: str = ALGORITHM
) -> dict[str, any] | None:
    try:
        return jwt.decode(jwt_token, public_key, algorithms=[algorithm])
    except jwt.InvalidTokenError as e:
        raise JWTDecodingError(f"JWT decoding failed: {e}") from e


@app.before_request
def log_request_info():
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())


@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


@app.route("/")
def hello_world():
    if session.get("authenticated"):
        return f"Hello, {session['email']}!"

    jwt_token = request.args.get("token")
    if jwt_token:
        decoded_token = decode_jwt_token(jwt_token, SERVER_PUBLIC_KEY)
        if decoded_token:
            session.permanent = True
            session["authenticated"] = True
            session["email"] = decoded_token["sub"]
            return redirect(url_for("hello_world"))

    # Fallback: Redirect to authentication
    data = {"app_id": APP_ID, "redirect_url": url_for("hello_world", _external=True)}
    jwt_token = generate_jwt_token(data, CLIENT_PRIVATE_KEY)
    return redirect(f"{MEMBRANE_SERVER}/authenticate?token={jwt_token}")


if __name__ == "__main__":
    app.run(debug=True)
