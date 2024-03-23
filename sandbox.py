import asyncio
import multiprocessing
import signal

from secret import discord_token
import web
import bot


def sigint_handler(sig, frame):
    print("Caught ctrl+c, terminating processes")
    bot_process.terminate()
    web_process.terminate()


if __name__ == "__main__":
    #bot_process = multiprocessing.Process(target=bot.begin, args=(discord_token,))
    bot_process = multiprocessing.Process(target=asyncio.run, args=(bot.begin(discord_token),))
    web_process = multiprocessing.Process(target=web.app.run, args=())

    bot_process.start()
    web_process.start()

    signal.signal(signal.SIGINT, sigint_handler)

    web_process.join()
    bot_process.join()
