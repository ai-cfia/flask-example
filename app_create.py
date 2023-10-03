from dotenv import load_dotenv
from quart import Quart
from quart_cors import cors
from quart_session import Session


def create_app():
    load_dotenv()
    app = Quart(__name__)
    app.config.update()
    app = cors(
        app,
        allow_origin="*"
    )
    Session(app)
    return app
