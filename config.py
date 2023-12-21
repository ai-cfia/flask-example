import os
from dataclasses import dataclass

from dotenv import load_dotenv

# Default values as constants
DEFAULT_LOGGING_LEVEL = "DEBUG"
DEFAULT_LOGGING_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
DEFAULT_SESSION_LIFETIME = 300
DEFAULT_TOKEN_EXPIRES_IN_SECONDS = 300
DEFAULT_APP_ID = "flask-example"
DEFAULT_REDIRECT_PATH = "/"

load_dotenv()


def read_membrane_key(membrane_server, env_variable):
    if membrane_server:
        with open(os.getenv(env_variable), "rb") as f:
            return f.read()


@dataclass
class Config:
    # Logging settings
    LOGGING_LEVEL = os.getenv("FLASK_EXAMPLE_LOGGING_LEVEL", DEFAULT_LOGGING_LEVEL)
    LOGGING_FORMAT = os.getenv("FLASK_EXAMPLE_LOGGING_FORMAT", DEFAULT_LOGGING_FORMAT)

    # Membrane related settings
    MEMBRANE_SERVER = os.getenv("FLASK_EXAMPLE_MEMBRANE_SERVER")
    SECRET_KEY = os.getenv("FLASK_EXAMPLE_SECRET_KEY")
    ALGORITHM = os.getenv("FLASK_EXAMPLE_ALGORITHM")
    SERVER_PUBLIC_KEY = read_membrane_key(
        MEMBRANE_SERVER, "FLASK_EXAMPLE_SERVER_PUBLIC_KEY_FILE"
    )
    CLIENT_PRIVATE_KEY = read_membrane_key(
        MEMBRANE_SERVER, "FLASK_EXAMPLE_CLIENT_PRIVATE_KEY_FILE"
    )
    PERMANENT_SESSION_LIFETIME = int(
        os.getenv("FLASK_EXAMPLE_SESSION_LIFETIME", DEFAULT_SESSION_LIFETIME)
    )
    TOKEN_EXPIRES_IN_SECONDS = int(
        os.getenv(
            "FLASK_EXAMPLE_TOKEN_EXPIRES_IN_SECONDS", DEFAULT_TOKEN_EXPIRES_IN_SECONDS
        )
    )
    APP_ID = os.getenv("FLASK_EXAMPLE_APP_ID", DEFAULT_APP_ID)
    REDIRECT_PATH = os.getenv("FLASK_EXAMPLE_REDIRECT_PATH", DEFAULT_REDIRECT_PATH)
