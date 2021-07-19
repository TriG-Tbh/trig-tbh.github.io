import discord

client = discord.Client()

@client.event
async def on_ready():
    print("go")

TOKEN = "[REDACTED]"

client.run(TOKEN, bot=False)