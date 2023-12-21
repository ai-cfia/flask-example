from flask import Flask
from membrane.client.flask import configure_membrane

from config import Config


def create_app(config: Config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Register the main blueprint
    from routes import blueprint as main_blueprint

    app.register_blueprint(main_blueprint)

    # Register Membrane's auth blueprint
    from membrane.client.flask import blueprint as membrane_blueprint

    app.register_blueprint(membrane_blueprint)

    # Configure Membrane login.
    certificate_data = {
        "app_id": config.APP_ID,
        "server_public_key": config.SERVER_PUBLIC_KEY,
        "client_private_key": config.CLIENT_PRIVATE_KEY,
        "auth_url": config.MEMBRANE_SERVER,
    }
    configure_membrane(
        app=app,
        certificate=certificate_data,
        token_expiration=config.TOKEN_EXPIRES_IN_SECONDS,
        custom_claims=None,
        landing_url=config.REDIRECT_PATH,
        logged_out_url=config.REDIRECT_PATH,
    )

    return app
