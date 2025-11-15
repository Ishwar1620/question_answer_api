#!/bin/bash

# Production startup script for QA API

set -e

echo "Starting QA API..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "Warning: .env file not found. Please create one from .env.example"
fi

# Create logs directory if it doesn't exist
mkdir -p logs

# Run the application
exec uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --workers 4 \
    --log-level info

