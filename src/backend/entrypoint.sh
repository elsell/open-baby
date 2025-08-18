#!/bin/bash

# Default to production environment
if [ -z "$ENVIRONMENT" ]; then
    ENVIRONMENT="prod"
fi

# Run the appropriate command
if [ "$ENVIRONMENT" = "dev" ]; then
    echo "Running in development mode"
    /app/venv/bin/fastapi dev main.py --host 0.0.0.0
else
    echo "Running in production mode"
    /app/venv/bin/fastapi run main.py --host 0.0.0.0
fi