import socket
import os
import asyncio
from collections import deque

import discord
from discord.ext import commands

from core import process_message, get_message_log, get_user, get_info

socket.gethostbyname("")
TOKEN = os.getenv('FRIEND_TOKEN_DISCORD')

# Create an instance of a bot
intents=discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)

message_queue = deque()

async def process_message_queue():
    while True:
        if message_queue:

            channel, content = message_queue.popleft()
            await channel.send(content)
        await asyncio.sleep(1)  # Send one message per second to avoid rate limits

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    bot.loop.create_task(process_message_queue())

@bot.event
async def on_message(message):

    try:
        if message.author == bot.user:
            return

        if message.content == '!crime':
            response = get_message_log(message.author)
            message_queue.append((message.channel, f'{response}'))
            return

        if message.content == '!info':
            response = get_info()
            amessage_queue.append((message.channel, f'{response}'))
            return

        if message.content.startswith('!ult'):
            return
                
        user_exist = get_user(message.author)

        response = process_message(message.content, message.author)
        if not response:
            return
        message_queue.append((message.channel, f'{message.author.mention} {response}'))

        if user_exist:
            await message.delete()

    except Exception as e:
        # Log the error or send a message to a specific channel for debugging
        print(f"An error occurred: {e}")

# Run the bot with the token
bot.run(TOKEN)