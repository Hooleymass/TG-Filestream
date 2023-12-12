from flask import Flask, request, jsonify, Response
from threading import Thread
from WebStreamer.__main__ import start_services, cleanup
import asyncio
import logging
import traceback

app = Flask(__name__)

# Route for the Telegram bot
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    try:
        # Forward the request to the Telegram bot logic
        response = handle_telegram_request(request)
        return jsonify(response)  # Assuming handle_telegram_request returns a dictionary
    except Exception as e:
        logging.error(f"Error in handling Telegram webhook: {e}")
        logging.error(traceback.format_exc())
        return jsonify({'error': 'Internal Server Error'}), 500

def run_telegram_bot(loop):
    try:
        logging.info("Starting Telegram bot...")
        loop.run_until_complete(start_services())
        logging.info("Telegram bot started successfully!")
    except Exception as err:
        logging.error(f"Error starting Telegram bot: {err}")
        logging.error(traceback.format_exc())
    finally:
        loop.stop()
        loop.run_until_complete(cleanup())
        logging.info("Stopped Telegram bot services")

# Route for testing bot connection
@app.route('/', methods=['POST'])
def post():
    if request.method == 'POST':
        # Access POST data from the request
        msg = request.get_json()

        print(msg)

        return jsonify({'status': 'ok'})

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    telegram_loop = asyncio.get_event_loop()
    telegram_thread = Thread(target=run_telegram_bot, args=(telegram_loop,))
    telegram_thread.start()

    # Run Flask on port 8080 using Gunicorn
    app.run(host='0.0.0.0', port=8080, debug=True)

