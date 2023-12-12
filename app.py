from flask import Flask, request
from threading import Thread
from WebStreamer.__main__ import start_services, cleanup
import asyncio
import logging

app = Flask(__name__)

# Route for the Telegram bot
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    # Forward the request to the Telegram bot logic
    response = handle_telegram_request(request)
    return response

# Route for the Flask API
@app.route('/api', methods=['GET'])
def flask_api():
    # Your Flask API logic here
    return 'Flask API Response'

def run_telegram_bot(loop):
    try:
        loop.run_until_complete(start_services())
    except Exception as err:
        logging.error(err.with_traceback(None))

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    telegram_loop = asyncio.get_event_loop()
    telegram_thread = Thread(target=run_telegram_bot, args=(telegram_loop,))
    telegram_thread.start()

    # Run Flask on port 5000 using Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)
