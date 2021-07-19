import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="/")

async def on_ready():
    print(bot.user.name)

token = "[REDACTED]"
bot.run(token)