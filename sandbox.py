import multiprocessing
from secret import discord_token
from web import app
from bot import bot


if __name__ == "__main__":
    bot_process = multiprocessing.Process(target=bot.run, args=(discord_token,))
    web_process = multiprocessing.Process(target=app.run, args=())
    bot_process.start()
    web_process.start()
