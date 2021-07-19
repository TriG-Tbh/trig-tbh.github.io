import discord

client = discord.Client()


@client.event
async def on_ready():
    print("ready")
    client.bot = True
    print(client.bot)

token = "[REDACTED]"


client.run(token, bot=False)