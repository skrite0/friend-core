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
    if message.author == bot.user:
        return

    if message.content == '!crime':
        response = get_message_log(message.author)
        await message.channel.send(f'{response}')
        return

    if message.content == '!info':
        response = get_info()
        await message.channel.send(f'{response}')
        return
            
    user_exist = get_user(message.author)

    response = process_message(message.content, message.author)
    if not response:
        return
    await message.channel.send(f'{message.author.mention} {response}')

    if user_exist:
        await message.delete()

# Run the bot with the token
bot.run(TOKEN)