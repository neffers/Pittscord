import discord

# get token from parent directory
import sys

sys.path.append('..')
from secret import discord_token

# local server channel IDs
bot_testing_channel_id = 1208576315070877706


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

        # Causes the bot to say "hello world" on load
        # await self.say_hello()

    async def on_message(self, message: discord.Message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        if message.author.dm_channel is None:
            await message.author.create_dm()

        if message.content.startswith('!hello'):
            await message.author.dm_channel.send(
                f"I saw your message at {message.created_at}, it was in the channel {message.channel}"
            )
            print(repr(message))

    async def say_hello(self):
        bot_testing_channel = self.get_channel(bot_testing_channel_id)
        await bot_testing_channel.send("Hello World!")


def make_bot():
    intents = discord.Intents.default()
    intents.message_content = True

    c = MyClient(intents=intents)
    return c, discord_token


if __name__ == '__main__':
    client, token = make_bot()
    client.run(token)
