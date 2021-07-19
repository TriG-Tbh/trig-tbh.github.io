
import pkg_resources
pkg_resources.require("discord==0.16.12")
pkg_resources.require("discord[voice]==0.16.12")
import pafy
from discord.ext import commands
import discord
import os
from settings import *
import asyncio

os.system("clear")

bot = commands.Bot(command_prefix=PREFIX)


def error(title, message):
    embed = discord.Embed(title=title, description=message, color=0xff0000)
    return embed

def success(title, message):
    embed = discord.Embed(title=title, description=message, color=0x00ff00)
    return embed


@bot.event
async def on_ready():
    print("Ready")


@bot.command(pass_context=True)
async def join(ctx):
    # test thing
    channel = ctx.message.author.voice.voice_channel
    if channel is None:
        return await bot.say(ctx.message.channel, embed=error("Could Not Connect to a Voice Channel", "You are not connected to a voice channel!"))
    asyncio.ensure_future(bot.join_voice_channel(channel))
    await bot.say(embed=success("Joined Voice Channel", "Successfully joined `{}`".format(channel.name)))
    




@bot.command(pass_context=True)
async def leave(ctx, aliases=['l', 'dis', 'disconnect', 'fuckoff']):
    server = ctx.message.server
    print(bot.is_voice_connected(server))
    
    voice_client = bot.voice_client_in(server)
    await voice_client.disconnect()




bot.run(TOKEN)
