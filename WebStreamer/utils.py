import asyncio
from threading import Thread
from flask import Flask

def run_flask_app(app: Flask):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    def run():
        app.run(host='0.0.0.0', port=5001)

    thread = Thread(target=run)
    thread.start()
    return thread

