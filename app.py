import os
from datetime import timedelta

from dotenv import load_dotenv
from flask import Flask, request
from membrane.client import (
    blueprint,
    configure,
    membrane_current_user,
    membrane_login_required,
)

load_dotenv()

# Constants
ACTIVATE_LOGIN = os.getenv("FLASK_EXAMPLE_ACTIVATE_LOGIN", "").lower() == "true"
SECRET_KEY = os.getenv("FLASK_EXAMPLE_SECRET_KEY")
SESSION_LIFETIME = int(os.getenv("FLASK_EXAMPLE_SESSION_LIFETIME", 300))
APP_ID = os.getenv("FLASK_EXAMPLE_APP_ID", "flask_example")
ALGORITHM = os.getenv("FLASK_EXAMPLE_ALGORITHM", "RS256")
SERVER_PUBLIC_KEY_FILE = os.getenv(
    "FLASK_EXAMPLE_SERVER_PUBLIC_KEY_FILE", "keys/server_public_key.pem"
)
CLIENT_PRIVATE_KEY_FILE = os.getenv(
    "FLASK_EXAMPLE_CLIENT_PRIVATE_KEY_FILE", "keys/client_private_key.pem"
)
TOKEN_EXPIRES_IN_SECONDS = int(os.getenv("FLASK_EXAMPLE_TOKEN_EXPIRES_IN_SECONDS", 300))
MEMBRANE_SERVER = os.getenv("FLASK_EXAMPLE_MEMBRANE_SERVER", "http://localhost:5000")

# Read key files at startup
with open(SERVER_PUBLIC_KEY_FILE, "rb") as file:
    SERVER_PUBLIC_KEY = file.read()

with open(CLIENT_PRIVATE_KEY_FILE, "rb") as file:
    CLIENT_PRIVATE_KEY = file.read()


# Initialize Flask and configuration
app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(seconds=SESSION_LIFETIME)


certificate_data = {
    "app_id": APP_ID,
    "server_public_key": SERVER_PUBLIC_KEY,
    "client_private_key": CLIENT_PRIVATE_KEY,
    "auth_url": MEMBRANE_SERVER,
}

configure(
    app,
    certificate_data,
    TOKEN_EXPIRES_IN_SECONDS,
    redirect_path="/",
    require_login=ACTIVATE_LOGIN,
)
app.register_blueprint(blueprint)


@app.before_request
def log_request_info():
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", request.get_data())


@app.route("/health", methods=["GET"])
def health():
    return "ok", 200


@app.route("/")
@membrane_login_required
def example_endpoint():
    user = membrane_current_user.id if hasattr(membrane_current_user, "id") else "world"
    return f"Hello, {user}!"


if __name__ == "__main__":
    app.run(debug=True)
