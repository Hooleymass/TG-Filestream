# This file is a part of TG-FileStreamBot
# Coding : Jyothis Jayanth [@EverythingSuckz]

import sys
import asyncio
import logging
from aiohttp import web
from pyrogram import idle
from flask import Flask, jsonify, request  # Add Flask imports
from WebStreamer import utils
from WebStreamer import StreamBot
from WebStreamer.server import web_server
from WebStreamer.bot.clients import initialize_clients

app = Flask(__name__)
stream_urls = []


@app.route('/')
def index():
    return 'Welcome to your streaming URLs app!'


@app.route('/save_url', methods=['POST'])
def save_url():
    data = request.json
    stream_url = data.get('url')
    if stream_url:
        stream_urls.append(stream_url)
        save_to_json()
        return jsonify(success=True)
    else:
        return jsonify(success=False, error='Invalid data')


@app.route('/display_urls')
def display_urls():
    return jsonify(stream_urls)


def save_to_json():
    with open('stream_urls.json', 'w') as file:
        file.write('\n'.join(stream_urls))


logging.basicConfig(
    level=logging.DEBUG if StreamBot.DEBUG else logging.INFO,
    datefmt="%d/%m/%Y %H:%M:%S",
    format="[%(asctime)s][%(name)s][%(levelname)s] ==> %(message)s",
    handlers=[logging.StreamHandler(stream=sys.stdout),
              logging.FileHandler("streambot.log", mode="a", encoding="utf-8")],)

server = web.AppRunner(web_server())
loop = asyncio.get_event_loop()


async def start_services():
    logging.info("Initializing Telegram Bot")
    await StreamBot.start()
    bot_info = await StreamBot.get_me()
    logging.debug(bot_info)
    StreamBot.username = bot_info.username
    logging.info("Initialized Telegram Bot")
    await initialize_clients()
    if StreamBot.KEEP_ALIVE:
        asyncio.create_task(utils.ping_server())
    await server.setup()
    await web.TCPSite(server, StreamBot.BIND_ADDRESS, StreamBot.PORT).start()
    logging.info("Service Started")
    logging.info("bot =>> {}".format(bot_info.first_name))
    if bot_info.dc_id:
        logging.info("DC ID =>> {}".format(str(bot_info.dc_id)))
    logging.info("URL =>> {}".format(StreamBot.URL))
    await idle()


async def cleanup():
    await server.cleanup()
    await StreamBot.stop()


if __name__ == "__main__":
    try:
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

