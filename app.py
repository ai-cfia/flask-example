"""
CFIA Flask Application
"""
import uuid
from datetime import datetime, timedelta

import jwt
from flask import Flask, redirect, request, session, url_for

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=300)


def generate_jwt(data, priv_key, headers=None):
    if "exp" not in data:
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        expiration_timestamp = int(expiration_time.timestamp())
        data["exp"] = int(expiration_timestamp)
    if headers is None:
        headers = {"alg": "RS256", "typ": "JWT", "app_id": "testapp1"}
    jwt_token = jwt.encode(data, priv_key, algorithm="RS256", headers=headers)
    return jwt_token


def decode_jwt_token(jwt_token, public_key):
    try:
        decoded_token = jwt.decode(jwt_token, public_key, algorithms=["RS256"])
        return decoded_token
    except Exception:
        print("jwt.decode failed")
        pass


@app.before_request
def log_request_info():
    """Log incoming request headers and body for debugging purposes."""
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())


@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


@app.route("/")
def hello_world():
    if session.get("authenticated"):
        email = session["decoded_token"]["sub"]
        return f"Hello, {email}!"

    jwt_token = request.args.get("token")
    if not jwt_token:
        with open("keys/client_private_key.pem", "rb") as file:
            private_key_content = file.read()

        expiration_time = datetime.utcnow() + timedelta(seconds=5 * 60)
        data = {
            "app_id": "flask_example",
            "redirect_url": url_for("hello_world", _external=True),
            "exp": int(expiration_time.timestamp()),
        }
        headers = {"alg": "RS256", "typ": "JWT", "app_id": "flask_example"}
        jwt_token = generate_jwt(data, private_key_content, headers)
        return redirect(f"http://127.0.0.1:5000/authenticate?token={jwt_token}")

    with open("keys/server_public_key.pem", "rb") as file:
        public_key_content = file.read()
    decoded_token = decode_jwt_token(jwt_token, public_key_content)
    if decoded_token:
        session.permanent = True
        session["authenticated"] = True
        session["decoded_token"] = decoded_token
        return redirect("http://localhost:4000/")

    return "Invalid Token!"


if __name__ == "__main__":
    app.run(debug=True)
