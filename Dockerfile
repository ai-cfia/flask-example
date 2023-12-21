FROM python:3.11

# Establish /code as working directory in the container
WORKDIR /app

# Copy the contents of the current directory into the container at /app
COPY . .

# Install project dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements-production.txt

# Use Gunicorn as the server, configuring it for the Flask app
ENTRYPOINT gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 --forwarded-allow-ips "*" app:app
