#!/bin/bash

# Default to production environment
if [ -z "$ENVIRONMENT" ]; then
    ENVIRONMENT="prod"
fi

# Run the appropriate command
if [ "$1" = "migrate" ]; then
    echo "Running database migrations"
    /app/venv/bin/alembic upgrade head
elif [ "$ENVIRONMENT" = "dev" ]; then
    echo "Running in development mode"
    /app/venv/bin/fastapi dev src/main.py --host 0.0.0.0
else
    echo "Running in production mode"
    /app/venv/bin/fastapi run src/main.py --host 0.0.0.0
fi