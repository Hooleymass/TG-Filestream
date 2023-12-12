#!/bin/env bash

sudo apk add --no-cache build-base python3-dev

# Start installing dependancy
echo "Start installing..."
pip install --no-cache-dir -r requirements.txt

# Start Flask app
echo "Starting Flask app..."
gunicorn app:app &

# Wait for Flask app to start (you might need to adjust the sleep duration)
sleep 5

# Start Bot
echo "Starting Bot..."
python3 -m WebStreamer
