import requests
import discord
import os
from dotenv import load_dotenv

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

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run(TOKEN)

'''
random = requests.get("https://api.scryfall.com/cards/random").json()
print("Nome: " + random["name"])
print("Custo de Mana: " + random["mana_cost"])
print("Texto: " + random["oracle_text"])
if "flavor_text" in random:
    print(random["flavor_text"])
'''