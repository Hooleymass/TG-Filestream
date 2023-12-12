from flask import Flask, request
from threading import Thread
from WebStreamer import __main__ as telegram_bot

app = Flask(__name__)

# Route for the Telegram bot
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    # Forward the request to the Telegram bot logic
    response = telegram_bot.handle_telegram_request(request)
    return response

# Route for the Flask API
@app.route('/api', methods=['GET'])
def flask_api():
    # Your Flask API logic here
    return 'Flask API Response'

def run_telegram_bot():
    # Run the Telegram bot
    telegram_bot.run_bot()

if __name__ == '__main__':
    # Start the Telegram bot in a separate thread
    telegram_thread = Thread(target=run_telegram_bot)
    telegram_thread.start()

    # Run Flask on port 5000 using Gunicorn
    app.run(host='0.0.0.0', port=5000, debug=True)

