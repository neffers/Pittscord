import asyncio
import discord
from quart import Quart
from secret import discord_token

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


# Execute the script
async def main():
    bot_task = asyncio.create_task(client.start(discord_token))
    web_task = asyncio.create_task(app.run_task())
    await web_task
    await bot_task


# WARNING: can't be stopped with ctrl+c
if __name__ == "__main__":
    asyncio.run(main())
