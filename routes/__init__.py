from flask import Blueprint, current_app, request
from membrane.client.flask import membrane_current_user, membrane_login_required

blueprint = Blueprint("main", __name__)


@blueprint.before_request
def log_request_info():
    current_app.logger.debug("Headers: %s", request.headers)
    current_app.logger.debug("Body: %s", request.get_data())


@blueprint.route("/health", methods=["GET"])
def health():
    return "ok", 200


@blueprint.route("/")
@membrane_login_required
def example_endpoint():
    user = membrane_current_user.id if hasattr(membrane_current_user, "id") else "world"
    return f"Hello, {user}!"
