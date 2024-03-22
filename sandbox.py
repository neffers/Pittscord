import asyncio
import multiprocessing
from secret import discord_token
import web
import bot


if __name__ == "__main__":
    #bot_process = multiprocessing.Process(target=bot.begin, args=(discord_token,))
    bot_process = multiprocessing.Process(target=asyncio.run, args=(bot.begin(discord_token),))
    web_process = multiprocessing.Process(target=web.app.run, args=())
    bot_process.start()
    web_process.start()
