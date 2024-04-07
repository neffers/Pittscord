import asyncio
import multiprocessing
import signal

import ipc_server
from secret import discord_token
import web


def sigint_handler(sig, frame):
    print("Caught ctrl+c, terminating processes")
    bot_process.terminate()
    web_process.terminate()


def start_server(token):
    asyncio.run(ipc_server.launch(token))


if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=start_server, args=(discord_token,))
    web_process = multiprocessing.Process(target=web.app.run, args=())

    bot_process.start()
    web_process.start()

    signal.signal(signal.SIGINT, sigint_handler)

    web_process.join()
    bot_process.join()
