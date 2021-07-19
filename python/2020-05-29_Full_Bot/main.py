import os
import discord
from discord.ext import commands

import cogs.mongohelper as mongo

prefix = mongo.find(mongo.SETTINGS, "prefix")["prefix"]
bot = commands.Bot(command_prefix=prefix)


@bot.event
async def on_ready():
    print("Ready")


path = os.path.dirname(os.path.realpath(__file__))
cogs = os.path.join(path, "cogs")

toload = mongo.find(mongo.SETTINGS, "cogs")

for file in os.listdir(cogs):
    if file.endswith(".py"):
        name = file[:-3]
        with open(os.path.join(cogs, file)) as f:
            content = f.read()
        if "# DNI" not in content:  # "DNI": Do Not Import
            if name not in toload["enabled"] and name not in toload["disabled"]:
                toload["enabled"].append(name)
mongo.update(mongo.SETTINGS, "cogs", {"enabled": toload["enabled"]})

for name in mongo.find(mongo.SETTINGS, "cogs")["enabled"]:
    bot.load_extension('cogs.{}'.format(name))

token = mongo.find(mongo.SETTINGS, "token")["token"]
bot.run(token)
