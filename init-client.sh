#!/bin/bash

set -e  # Exit on error
set -x  # Debug mode

# Create keys directory if it doesn't exist
mkdir -p keys

# Generate client keys
openssl genpkey -algorithm RSA -out "keys/client_private_key.pem" >> init.log 2>&1
openssl rsa -pubout -in "keys/client_private_key.pem" -out "keys/client_public_key.pem" >> init.log 2>&1


echo "Server keys generated in 'keys' folder."

# Copy .env.template to .env
cp .env.template .env >> init.log 2>&1

# Copy .env.tests.template to .env.tests
cp .env.tests.template .env.tests >> init.log 2>&1

echo "Environment files generated."
