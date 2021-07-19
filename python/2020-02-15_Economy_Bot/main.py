import discord
from discord.ext import commands

import settings

import importlib
import time
import json
import random
import asyncio
import os
path = os.path.dirname(os.path.realpath(__file__))


def join(name):
    return os.path.join(path, name)

def botembed(title):
    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.set_author(name=title)
    return embed

bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command("help")

def read_coins(id):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            return None
        else:
            return values[id]
        
def add_coins(id, amount):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            values[id] = 0
        values[id] += amount
        with open(join("economy.json"), "w") as nf:
            json.dump(values, nf)

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        formatted = time.strftime("%H:%M:%S", time.gmtime(error.retry_after))
        embed = botembed("Cooldown")
        embed.add_field(name="Slow down, there!", value="This command is on cooldown for {}. Try again later!".format(formatted))
        return await ctx.send(embed=embed)
    else:
        raise error

@bot.event
async def on_message(message):
    authorid = str(message.author.id)
    ctx = await bot.get_context(message)
    if ctx.valid:
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            await bot.process_commands(message)
    elif not message.author.bot and not isinstance(message.channel, discord.abc.PrivateChannel):
        getgold = False
        with open(join("economy.json")) as f:
            values = json.load(f)
            if authorid not in values.keys():
                values[authorid] = 0
                with open(join("delay.json")) as f:
                    delays = json.load(f)
                    delays[authorid] = time.time()
                    with open(join("delay.json"), "w") as nf:
                        json.dump(delays, nf)
                getgold = True

            else:
                with open(join("delay.json")) as f:
                    delays = json.load(f)
                    now = time.time()
                    if authorid not in delays.keys():
                        delays[authorid] = now
                        getgold = True
                    else:
                        previous = delays[authorid]
                        if now - previous >= settings.DELAY:
                            delays[authorid] = now
                            getgold = True
                    with open(join("delay.json"), "w") as nf:
                        json.dump(delays, nf)
        
            if getgold:
                values[authorid] += 1 # Temporary value, will switch to something else

                with open(join("economy.json"), "w") as nf:
                    json.dump(values, nf)
    
    dropped = random.randint(1, 50)
    #dropped = 25
    if dropped == 25 and not isinstance(message.channel, discord.abc.PrivateChannel):
        if read_coins(message.author.id) is not None: 
            if read_coins(message.author.id) > 0:
                amount = random.randint(1, read_coins(message.author.id) // 2)
                add_coins(message.author.id, -amount)
                values = [c for c in "0123456789"]
                code = ""
                for _ in range(4):
                    code += random.choice(values)
                def check(message):
                    return message.content == code and message.channel == ctx.message.channel
                embed = botembed("Random Event")
                embed.add_field(name="Coin{} ha{} been dropped!".format(("s" if amount != 1 else ""), ("ve" if amount != 1 else "s")), value="While typing, <@{}> dropped **{} coin{}**! First person to type the code `{}` within 10 seconds gets the coin{}!".format(message.author.id, amount, ("s" if amount != 1 else ""), code, ("s" if amount != 1 else "")))
                message = await ctx.send(embed=embed)
                try:
                    newmessage = await bot.wait_for("message", check=check, timeout=10.0)
                except asyncio.TimeoutError:
                    embed = botembed("Random Event")
                    embed.add_field(name="Coin{} lost...".format(("s" if amount != 1 else "")), value="Nobody picked up the **{} coin{}**.".format(amount, ("s" if amount != 1 else "")))
                    await message.edit(embed=embed)
                else:
                    embed = botembed("Random Event")
                    embed.add_field(name="Coin{} picked up!".format(("s" if amount != 1 else "")), value="<@{}> picked up the **{} coin{}**!".format(newmessage.author.id, amount, ("s" if amount != 1 else "")))
                    await message.edit(embed=embed)
                    add_coins(newmessage.author.id, amount)

@bot.command()
async def help(ctx, cog=None):
    embed = botembed("Help (General)")
    if cog is not None:
        for filename in os.listdir(f'{path}/cogs'):
            if filename == cog + ".py":
                imported = importlib.import_module("cogs.{}".format(cog))
                embed = imported.helpembed(settings.PREFIX)
                return await ctx.send(embed=embed)
    else:
        for filename in os.listdir(f'{path}/cogs'):
            if filename.endswith(".py"):
                embed.add_field(name=filename[:-3].capitalize(), value="Use the command `{}help {}` to see the available commands in this category.".format(settings.PREFIX, filename[:-3]))
        return await ctx.send(embed=embed)


for filename in os.listdir(f'{path}/cogs'):
    if filename.endswith(".py") and not filename.startswith("__init__"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(settings.TOKEN)