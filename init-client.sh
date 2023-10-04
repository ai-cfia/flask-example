#!/bin/bash

set -e  # Exit on error
set -x  # Debug mode

# Create keys directory if it doesn't exist
mkdir -p keys

# Generate test keys
openssl genpkey -algorithm RSA -out "tests/test_keys/private_key.pem" >> init.log 2>&1
openssl rsa -pubout -in "tests/test_keys/private_key.pem" -out "tests/test_keys/public_key.pem" >> init.log 2>&1

echo "Test keys generated in 'tests/test_keys' folder."

# Copy .env.template to .env
cp .env.template .env >> init.log 2>&1

echo "Environment files generated."
