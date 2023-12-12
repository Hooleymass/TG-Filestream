#!/bin/bash

# Start Flask app
echo "Starting Flask app..."
gunicorn app:app &

# Wait for Flask app to start (you might need to adjust the sleep duration)
sleep 5

# Start Bot
echo "Starting Bot..."
python3 -m WebStreamer
