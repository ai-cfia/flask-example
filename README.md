# flask-example

A minimal flask app to test membrane.

# Installation

1. Clone the repository:

```bash
git clone https://github.com/ai-cfia/flask-example.git
```

2. Open in devcontainer.

Alternatively,

1. Clone the repository:

```bash
git clone https://github.com/ai-cfia/flask-example.git
cd flask-example
```

2. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install the dependencies:

```bash
pip install -r requirements.txt
```

# Usage

## Running and testing the API

Create and set the environment variables based on `.env.template`.

### Running:

```
flask run -h 0.0.0.0 --debug
```

### Check health

```
curl -X GET http://localhost:5000/health"
```

Expect: `ok`.

### Request the main route "/":

```
curl -X GET http://localhost:5000/"
```

Expect to be redirected to `membrane-frontend` if you haven't logged in yet, `Hello, {user}!` if you have.

# Deployment

## Azure
Create and set the environment variables based on `.env.template`.

Build (do this from your WSL Ubuntu where Docker is already installed):

```
docker build -t flask-example .
```

test locally:

```
export PORT=<your_port_here>
docker run -v $(pwd)/keys:/app/keys -p $PORT:$PORT -e PORT=$PORT --env-file .env flask-example
```
