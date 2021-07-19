import settings
import os
import importlib

functions = importlib.import_module("cogs.functions")

path = os.path.dirname(os.path.realpath(__file__))

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Ready")

@bot.command()
async def help(ctx, cog=None):
    embed = functions.embed("Help")
    if cog is not None:
        for filename in os.listdir(os.path.join(path, "cogs")):
            if filename.endswith(".py") and filename == cog + ".py" and not filename.endswith("functions.py"):
                imported = importlib.import_module("cogs.{}".format(cog))
                embed = imported.help(settings.PREFIX)
                return await ctx.send(embed=embed)
    else:
        for filename in os.listdir(os.path.join(path, "cogs")):
            if filename.endswith(".py"):
                embed.add_field(name=filename[:-3].capitalize(), value="Use the command `{}help {}` to see the available commands in this category.".format(settings.PREFIX, filename[:-3]))
        return await ctx.send(embed=embed)


for filename in os.listdir(os.path.join(path, "cogs")):
    if filename.endswith(".py"):
        bot.load_extension("cogs.{}".format(filename[:-3]))

bot.run(settings.TOKEN)