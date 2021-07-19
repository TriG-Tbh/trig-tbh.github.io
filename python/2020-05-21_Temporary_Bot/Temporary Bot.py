import asyncio
import discord
from discord.ext import commands
import datetime

bot = commands.Bot(command_prefix="whenthe")
bot.remove_command("help")

red = 0xff470f
blue = 0x117ea6
green = 0x23d160


def botembed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.timestamp = datetime.datetime.utcnow()
    return embed


@bot.event
async def on_ready():
    user = await bot.fetch_user(610575567041069097)
    print(str(user.avatar_url_as(format="png")))

token = "[REDACTED]"
bot.run(token)
