from flask import Flask
from membrane.client import configure_membrane

from config import Config


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Register the main blueprint
    from main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    # Register Membrane's auth blueprint
    from membrane.client import blueprint as membrane_blueprint

    app.register_blueprint(membrane_blueprint)

    # Configure Membrane login.
    certificate_data = {
        "app_id": config.APP_ID,
        "server_public_key": config.SERVER_PUBLIC_KEY,
        "client_private_key": config.CLIENT_PRIVATE_KEY,
        "auth_url": config.MEMBRANE_SERVER,
    }
    configure_membrane(
        active=bool(config.MEMBRANE_SERVER),
        app=app,
        certificate=certificate_data,
        token_expiration=config.TOKEN_EXPIRES_IN_SECONDS,
        custom_claims=None,
        redirect_path=config.REDIRECT_PATH,
    )

    return app