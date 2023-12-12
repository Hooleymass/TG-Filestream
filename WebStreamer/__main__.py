import sys
import asyncio
import logging
import json
from .vars import Var
from aiohttp import web
from pyrogram import idle
from WebStreamer import utils
from WebStreamer import StreamBot
from WebStreamer.server import web_server
from WebStreamer.bot.clients import initialize_clients
from flask import Flask, jsonify  # Added Flask import

logging.basicConfig(
    level=logging.DEBUG if Var.DEBUG else logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)

logging.getLogger("aiohttp").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.INFO if Var.DEBUG else logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.DEBUG if Var.DEBUG else logging.ERROR)

# Added list to store generated URLs
generated_urls = []

server = web.AppRunner(web_server())
app = Flask(__name__)  # Initialize Flask app

loop = asyncio.get_event_loop()


async def start_services():
    logging.info("Initializing Telegram Bot")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    logging.debug(bot_info)
    StreamBot.username = bot_info.username
    logging.info("Initialized Telegram Bot")
    await initialize_clients()
    if Var.KEEP_ALIVE:
        asyncio.create_task(utils.ping_server())
    await server.setup()
    await web.TCPSite(server, Var.BIND_ADDRESS, Var.PORT).start()
    logging.info("Service Started")
    logging.info("bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        logging.info("DC ID =>> {}".format(str(bot_info.dc_id)))
    logging.info("URL =>> {}".format(Var.URL))

    # Append the generated URL to the list
    generated_urls.append(Var.URL)

    await idle()


async def cleanup():
    await server.cleanup()
    await StreamBot.stop()

    # Save the list of generated URLs to a JSON file
    with open("generated_urls.json", "w") as json_file:
        json.dump(generated_urls, json_file, indent=2)


# Flask route to serve the generated URLs
@app.route('/api/generated_urls', methods=['GET'])
def get_generated_urls():
    return jsonify(generated_urls)


if __name__ == "__main__":
    try:
        # Run Flask app in a separate thread
        import threading
        flask_thread = threading.Thread(target=app.run, kwargs={'port': 5000, 'debug': False})
        flask_thread.start()

        # Run asyncio loop for the main functionality
        loop.run_until_complete(start_services())

    except KeyboardInterrupt:
        pass
    except Exception as err:
        logging.error(err.with_traceback(None))
    finally:
        try:
            loop.run_until_complete(cleanup())
        except Exception as err:
            logging.error(err.with_traceback(None))
        finally:
            loop.stop()
            logging.info("Stopped Services")

