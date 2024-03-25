import discord
import json
import re
from discord import app_commands
from discord.ext import commands

import database
from secret import db_filename

intents = discord.Intents.all()

# For Testing Purposes
bot_testing_channel_id = 1208576315070877706


# Custom Bot Class Definition
class PittscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db = database.Database(db_filename)

    def generate_server_json(self, server_id: int) -> str:
        """Generates a simple json list of the server's channel structure and returns it as a string"""
        guild = self.get_guild(server_id)
        if guild is None:
            raise KeyError

        channels = guild.by_category()
        json_channels = []

        for category, chan_list in channels:
            if category is None:
                parent = json_channels
            else:
                cat = {
                    'name': category.name,
                    'type': 'category',
                    'channels': []
                }
                json_channels.append(cat)
                parent = cat['channels']

            for chan in chan_list:
                match type(chan):
                    case discord.TextChannel:
                        chan_type = 'text'
                    case discord.VoiceChannel:
                        chan_type = 'voice'
                    case discord.ForumChannel:
                        chan_type = 'forum'
                    case discord.StageChannel:  # unlikely but possible
                        chan_type = 'stage'
                    case _:
                        chan_type = None

                c = {
                    'name': chan.name,
                    'type': chan_type,
                }

                parent.append(c)

        return json.dumps(json_channels)

    # send message to testing channel
    async def say_hello(self):
        bot_testing_channel = self.get_channel(bot_testing_channel_id)
        await bot_testing_channel.send("Hello World!")

    async def process_semester_config(self, config: str):
        #TODO: implement based on received config
        raise NotImplementedError


bot = PittscordBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is successfully logged in and ready to accept commands.
    May also run after network failures? Don't use it to schedule things. (That's why there's a !sync command)"""
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member: discord.Member):
    if member.dm_channel is None:
        await member.create_dm()
    if bot.db.get_student_id(member.id) is None:
        await member.dm_channel.send(f'Hi! I don\'t recognize you! Can you send me your Pitt ID? It looks like `abc123`.')

        def check(m):
            return m.channel == member.dm_channel and m.author == member

        pitt_id_regex = re.compile('[a-z]{3}\d+')
        while True:
            msg = await bot.wait_for('message', check=check)
            pittid = pitt_id_regex.fullmatch(msg.content.lower())
            if pittid is not None:
                break
            else:
                await member.dm_channel.send(f'I don\'t recognize that, please try again.')

        bot.db.add_student(pittid, member.id)
        await member.dm_channel.send(f'Thanks!')
    # TODO: find the student in classes and add to roles


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def identify(interaction: discord.Interaction, user: discord.User):
    """Look up a user's Pitt ID. Currently only responds with Discord ID."""
    student_id = bot.db.get_student_id(user.id)
    await interaction.response.send_message(f"{student_id}", ephemeral=True)


@identify.error
async def identify_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """Runs when the identify function encounters some error."""
    if interaction.user.guild_permissions.administrator:
        response = "Encountered some unknown error! Check the logs for more."
        print(repr(error))
    else:
        response = "You are not authorized to use that command! This incident will be recorded."
        print(f"User {interaction.user.name} tried to use identify.")
    await interaction.response.send_message(response, ephemeral=True)


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def deregister(interaction: discord.Interaction, user: discord.User):
    """Remove an association of pitt id from discord id"""
    student_id = bot.db.get_student_id(user.id)
    bot.db.remove_student_association(user.id)
    await interaction.response.send_message(f"Removed association with {student_id}", ephemeral=True)


@bot.command()
async def sync(interaction: discord.Interaction):
    """Command to re-register 'app_commands' (slash commands) with Discord so that they can be used.
    Shouldn't need to use this command usually, only during development?"""
    print("Attempting to sync global commands")
    globalsync = await bot.tree.sync()
    print(f"global sync returned:\n{globalsync}")
    if interaction.guild is not None:
        print("Attempting to sync guild commands")
        localsync = await bot.tree.sync(guild=interaction.guild)
        print(f"local sync returned:\n{localsync}")


@bot.command()
async def serverjson(interaction: discord.Interaction):
    print(bot.generate_server_json(interaction.guild.id))


if __name__ == "__main__":
    from secret import discord_token
    bot.run(discord_token)
