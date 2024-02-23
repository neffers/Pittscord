import discord
from discord import app_commands
from discord.ext import commands
from secret import discord_token

intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.tree.command()
@app_commands.guild_only()
@app_commands.default_permissions(administrator=True)
@app_commands.checks.has_permissions(administrator=True)
async def identify(interaction: discord.Interaction, user: discord.User):
    await interaction.response.send_message(f"{user.id}", ephemeral=True)


@identify.error
async def identify_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    if interaction.user.guild_permissions.administrator:
        response = "Encountered some unknown error! Check the logs for more."
        print(repr(error))
    else:
        response = "You are not authorized to use that command! This incident will be recorded."
        print(f"User {interaction.user.name} tried to use identify.")
    await interaction.response.send_message(response, ephemeral=True)


@bot.command()
async def sync(interaction: discord.Interaction):
    print("Attempting sync")
    globalsync = await bot.tree.sync()
    localsync = await bot.tree.sync(guild=interaction.guild)
    print(f"global sync returned:\n{globalsync}\n\nlocal sync returned:\n{localsync}")

bot.run(discord_token)
