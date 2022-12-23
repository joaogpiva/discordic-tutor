import discord
import os
from dotenv import load_dotenv
from functions import *

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('s!'):
        name = message.content[3:]
        try:
            card = fuzzySearch(name)
            await message.channel.send(printSimple(card))
        except Exception as e:
            await message.channel.send(e)

    if message.content.startswith('r!'):
        random = getRandomCard()
        await message.channel.send(printSimple(random))

client.run(TOKEN)