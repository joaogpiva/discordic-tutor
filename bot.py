import discord
import os
import urllib
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

    if message.content[1] == "!":
        prefixLength = 3
        hasImage = extended = prices = False
        card = None
        wrongSpelling = False

        if " -i" in message.content:
            hasImage = True
            prefixLength += 3

        if " -e" in message.content:
            extended = True
            prefixLength += 3

        if " -p" in message.content:
            prices = True
            prefixLength += 3

        if message.content[0] == "s":
            name = message.content[prefixLength:]

            try:
                card = fuzzySearch(name)
                layout = findLayout(card)

                if hasImage:
                    if layout == 2:
                        faceCount = 0
                        for face in card["card_faces"]:
                            urllib.request.urlretrieve(card["card_faces"][faceCount]["image_uris"]["normal"], "card" + str(faceCount) + ".jpg")
                            faceCount += 1
                    else:
                        urllib.request.urlretrieve(card["image_uris"]["normal"], "card.jpg")
                    
            except Exception as e:
                await message.channel.send(e)
                wrongSpelling = True

        if message.content[0] == "r":
            try:
                card = getRandomCard()
                if hasImage:
                    urllib.request.urlretrieve(card["image_uris"]["normal"], "card.jpg")
            except Exception as e:
                await message.channel.send(e)

        if card:

            if layout == 0:
                if hasImage:
                    await message.channel.send(printSimple(card), file=discord.File("card.jpg"))
                else:
                    await message.channel.send(printSimple(card))
            elif layout == 1:
                faceCount = 0
                for face in card["card_faces"]:
                    if faceCount == len(card["card_faces"]) - 1 and hasImage:
                        await message.channel.send("Face " + str(faceCount + 1) + ":\n\n" + printSimple(face), file=discord.File("card.jpg"))
                    else:
                        await message.channel.send("Face " + str(faceCount + 1) + ":\n\n" + printSimple(face))
                    faceCount += 1
            elif layout == 2:
                faceCount = 0
                for face in card["card_faces"]:
                    if hasImage:
                        await message.channel.send("Face " + str(faceCount + 1) + ":\n\n" + printSimple(face), file=discord.File("card" + str(faceCount) + ".jpg"))
                    else:
                        await message.channel.send("Face " + str(faceCount + 1) + ":\n\n" + printSimple(face))
                    faceCount += 1

        elif not card and not wrongSpelling:
            await message.channel.send("Something didn't quite work... Please try again or, if the error persists, report this on Github (https://github.com/joaogpiva/untitled-scryfall-fetcher) or send the dev a DM (Piva#1177).")
        
        for filename in os.listdir("./"):
            if filename.endswith("jpg"):
                os.remove(filename)

client.run(TOKEN)