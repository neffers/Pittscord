import discord
import json
import re
from discord import app_commands
from discord.ext import commands

#import database
import pretend_database as database
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

    async def semester_cleanup(self):
        # TODO
        # get current semester roles and move those students to "previous student" role
        # delete the old roles
        # delete the old channels (saving logs?)
        raise NotImplementedError


bot = PittscordBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is successfully logged in and ready to accept commands.
    May also run after network failures? Don't use it to schedule things. (That's why there's a !sync command)"""
    print(f'We have logged in as {bot.user}')


@bot.event
async def on_member_join(member: discord.Member):
    """A method that runs when a user joins a guild the bot is in."""
    # We're probably going to send this user some messages, so make sure that the dm channel exists
    if member.dm_channel is None:
        await member.create_dm()

    # Check for the user's presence in the database (in case of a leave-rejoin)
    if bot.db.get_student_id(member.id) is None:
        await member.dm_channel.send(f'Hi! I don\'t recognize you! Can you send me your Pitt ID? It looks like `abc123`.')

        def check(m):
            return m.channel == member.dm_channel and m.author == member

        # Matches three alphabetic characters followed at least one numeric digit
        pitt_id_regex = re.compile('[a-z]{3}\d+')

        while True:
            msg = await bot.wait_for('message', check=check)
            pittid = pitt_id_regex.fullmatch(msg.content.lower())
            if pittid is not None:
                pittid = pittid.string
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
    if student_id is None:
        await interaction.response.send_message(f"No pitt id available!", ephemeral=True)
    else:
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


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
async def ask_user_to_register(interaction: discord.Interaction, user: discord.User):
    """Ask user to identify themselves to the bot"""
    await interaction.response.send_message("Asking!", ephemeral=True)
    await on_member_join(user)


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
    """Development command, so I can see what json I'm making"""
    print(bot.generate_server_json(interaction.guild.id))


if __name__ == "__main__":
    from secret import discord_token
    bot.run(discord_token)
