from flask import Flask
import discord
from secret import discord_token
from threading import Thread

app = Flask(__name__)

# local server channel IDs
bot_testing_channel_id = 1208576315070877706


class Pittscord(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def say_hello(self):
        bot_testing_channel = self.get_channel(bot_testing_channel_id)
        await bot_testing_channel.send("Hello World!")


# setup discord bot client
intents = discord.Intents.default()
intents.message_content = True

client = Pittscord(intents=intents)


@app.route("/")
async def default():
    await client.say_hello()
    return ""


def run_bot():
    # DON'T USE RUN!!!
    client.run(discord_token)


def run_flask():
    # maybe don't use run??
    app.run()


if __name__ == "__main__":
    pass
