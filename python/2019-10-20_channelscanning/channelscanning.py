import discord
import os

os.system("clear")

client = discord.Client()

print("Logging in...")

words = []
gcharacters = []

@client.event
async def on_ready():
    print("Getting words...")
    blacklist = "`1234567890-=~!@#$%^&*()_+[]\\{}|;':\",./<>? "
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    with open("/usr/share/dict/words", "r") as f:
        words = ["".join([letter for letter in word.lower() if letter not in blacklist]) for word in f.read().split("\n")]

    serverid = "[REDACTED]"

    server = await client.fetch_guild(serverid)
    for channel in server.channels:
        print()
        channelid = channel.id
        print("Getting messages from {}...".format(channel.name))
        channel = client.get_channel(channelid)
        messages = await channel.history(limit=None).flatten()
        print("Scanning messages...")
        for message in messages:
            content = message.content.lower()
            content = content.replace("\n", " ")
            messagewords = content.split(" ")
            for word in messagewords:
                for _ in range(len(word)):
                    i = 0
                    word = list(word)
                    for letter in word:
                        if letter not in alphabet:
                            del word[i]
                        i += 1
                word = "".join(word)
                if word not in words:
                    if word not in gcharacters:
                        gcharacters.append(word)
                        #input("GOOD: " + word)

    print("\n".join(gcharacters))
    print("\n-----------------\nDONE")



token = "[REDACTED]"
client.run(token, bot=False)
