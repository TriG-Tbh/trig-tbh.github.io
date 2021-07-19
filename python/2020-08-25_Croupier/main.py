import discord
import os
import sys
from discord.ext import commands
import cogs.settings as settings
import cogs.mongohelper as mh
import cogs.functions as functions
import humanize
import datetime as dt


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    async def on_ready(self):
        user = self.user
        print(f"Logged in as: {user.name}#{user.discriminator}")
    

bot = Bot(command_prefix=settings.PREFIX)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        cooldown = error.cooldown
        num = cooldown.rate
        limit = cooldown.per
        retry_after = error.retry_after
        embed = functions.error(f"⏱️ Slow down! This command can be used `{num}x` every {functions.humanize(dt.timedelta(seconds=limit))}. You can use this command again in {functions.humanize(dt.timedelta(seconds=retry_after))}.")
        await ctx.send(embed=embed)

path = os.path.dirname(os.path.realpath(__file__))
cogs = os.path.join(path, "cogs")
sys.path.append(os.path.join(path, "cogs"))

for file in os.listdir(cogs):
    if file.endswith(".py"):
        name = file[:-3]
        with open(os.path.join(cogs, file), encoding="utf-8") as f:
            try:
                content = f.read()
            except:
                print(name)
        if "# DNI" not in content:  # "DNI": Do Not Import
            bot.load_extension("cogs." + name)

bot.run(settings.TOKEN)