import socket
import os

import discord
from discord.ext import commands

from core import process_message

socket.gethostbyname("")
TOKEN = os.getenv('FRIEND_TOKEN_DISCORD')

# Create an instance of a bot
intents=discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    response = process_message(message.content)
    if not response:
        return
    await message.channel.send(f'{message.author.mention}{response}')

# Run the bot with the token
bot.run(TOKEN)