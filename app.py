"""
CFIA Quart Application
"""
from datetime import datetime, timedelta
import jwt
from quart import request, session, url_for, redirect
from app_create import create_app


app = create_app()
app.secret_key = "secret"

def generate_jwt(data, priv_key, headers=None):
    if 'exp' not in data:
        expiration_time = datetime.utcnow() + timedelta(minutes=30)
        expiration_timestamp = int(expiration_time.timestamp())
        data['exp'] = int(expiration_timestamp)
    if headers is None:
        headers = {
            "alg": "RS256",
            "typ": "JWT",
            "app_id": "testapp1"
        }
    jwt_token = jwt.encode(data, priv_key, algorithm='RS256', headers=headers)
    return jwt_token


def decode_jwt_token(jwt_token, public_key):
    try:
        decoded_token = jwt.decode(jwt_token, public_key, algorithms=['RS256'])
        return decoded_token
    except Exception:
        print("jwt.decode failed")
        pass
    

@app.before_request
async def log_request_info():
    """Log incoming request headers and body for debugging purposes."""
    app.logger.debug("Headers: %s", request.headers)
    app.logger.debug("Body: %s", await request.get_data())


@app.route("/health", methods=["GET"])
async def health():
    return "ok", 200


@app.route('/')
def hello_world():
    if 'authenticated' in session and session['authenticated']:
        email = session['decoded_token']['sub']
        return f'Hello, {email}!'
    
    jwt_token = request.args.get('token')
    if not jwt_token:
        with open('keys/client_private_key.pem', 'rb') as file:
            private_key_content = file.read()
        data = {
            "app_id": "flask_example",
            "redirect_url": url_for("hello_world", _external=True)
        }
        jwt_token = generate_jwt(data, private_key_content)
        print("redirect1")
        return redirect(f"http://127.0.0.1:5000/authenticate?token={jwt_token}")
    
    with open('keys/server_public_key.pem', 'rb') as file:
        public_key_content = file.read()
    decoded_token = decode_jwt_token(jwt_token, public_key_content)
    if decoded_token:
        session.permanent = True
        session['authenticated'] = True
        session['decoded_token'] = decoded_token
        print("redirect2")
        return redirect(url_for("hello_world"))
    
    return 'Invalid Token!'


if __name__ == "__main__":
    app.run(debug=True)
