import socket
import os

import discord
from discord.ext import commands

from core import process_message, get_message_log, get_user, get_info

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
    if message.author == bot.user or not message.content:
        return

    response = process_message(message.content, message.author)

    if not response or response['code'] == 0:
        return
    elif response['code'] == 1:
        await message.delete()
    elif response['code'] == 4:
        return

    await message.channel.send(f'{response['message']}')
    return

# Run the bot with the token
bot.run(TOKEN)