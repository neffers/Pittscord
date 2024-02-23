import asyncio

import discord
from discord import app_commands
from discord.ext import commands

# get token from parent directory
import sys

sys.path.append('..')
from secret import discord_token


intents = discord.Intents.all()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')


@bot.tree.command()
@app_commands.checks.has_permissions(administrator=True)
async def identify(interaction: discord.Interaction, user: discord.User):
    print("in identify func")
    await interaction.response.send_message(f"{user.id}", ephemeral=True)


@bot.command()
async def sync(interaction: discord.Interaction):
    print("Attempting sync")
    globalsync = await bot.tree.sync()
    localsync = await bot.tree.sync(guild=interaction.guild)
    print(f"global sync returned:\n{globalsync}\n\nlocal sync returned:\n{localsync}")

bot.run(discord_token)