from quart import Quart
import discord
from secret import discord_token
from threading import Thread

app = Quart(__name__)

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


async def run_bot():
    client.run(discord_token)


async def run_flask():
    app.run()


if __name__ == "__main__":
    bot_thread = Thread(target=run_bot())
    flask_thread = Thread(target=run_flask())

    bot_thread.run()
    flask_thread.run()

    bot_thread.join()
    flask_thread.join()