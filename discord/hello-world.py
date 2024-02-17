import discord

# get token from parent directory
import sys
sys.path.append('..')
from secret import discord_token


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        #if message.author.dm_channel is None:
            #await message.author.create_dm()

        if message.content.startswith('!hello'):
            await message.author.dm_channel.send(
                f"I saw your message at {message.created_at}, it was in the channel {message.channel}"
            )
            print(repr(message))


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(discord_token)
