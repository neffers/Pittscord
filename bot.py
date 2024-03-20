import discord
import json
from discord import app_commands
from discord.ext import commands
from secret import discord_token

intents = discord.Intents.all()


class PittscordBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


bot = PittscordBot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    """Runs when the bot is successfully logged in and ready to accept commands.
    May also run after network failures? Don't use it to schedule things. (That's why there's a !sync command)"""
    print(f'We have logged in as {bot.user}')


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def identify(interaction: discord.Interaction, user: discord.User):
    """Look up a user's Pitt ID. Currently only responds with Discord ID."""
    await interaction.response.send_message(f"{user.id}", ephemeral=True)


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


bot.run(discord_token)
