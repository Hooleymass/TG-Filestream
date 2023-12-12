# run.py

import subprocess
import time

def start_flask_app():
    print("Starting Flask app...")
    subprocess.Popen(["gunicorn", "--bind", ":8080", "--workers", "2", "app:app"])

def start_bot():
    print("Starting Bot...")
    subprocess.Popen(["python3", "-m", "WebStreamer"])

if __name__ == "__main__":
    start_flask_app()
    
    # Wait for Flask app to start (you might need to adjust the sleep duration)
    time.sleep(5)
    
    start_bot()

