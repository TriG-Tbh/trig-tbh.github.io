
import asyncio
from settings import *
import os
import discord
from discord.ext import commands
import pafy
import pkg_resources
pkg_resources.require("discord==0.16.12")
pkg_resources.require("discord[voice]==0.16.12")

os.system("clear")

bot = commands.Bot(command_prefix=PREFIX)


bot.remove_command("help")


def error(title, message):
    embed = discord.Embed(title="Error Message", color=0xff0000)
    embed.add_field(name="Error", value=title, inline=False)
    embed.add_field(name="Reason", value=message, inline=False)
    return embed


def success(title, message):
    embed = discord.Embed(title="Success Message", color=0x00ff00)
    embed.add_field(name="Successful Action", value=title, inline=False)
    embed.add_field(name="Message", value=message, inline=False)
    return embed


@bot.event
async def on_ready():
    print("Ready")


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.voice_channel
    if channel is None:
        return await bot.say(embed=error("Could not connect to a voice channel", "You are not connected to a voice channel!"))
    try:
        
        asyncio.ensure_future(bot.loop.run_until_complete(bot.join_voice_channel(channel)))
    except Exception as e:
        return await bot.say(embed=error("Could not connect to a voice channel", str(e)))
    await bot.say(embed=success("Joined voice channel", "Successfully joined `{}`".format(channel.name)))


@bot.command(pass_context=True)
async def leave(ctx):
    server = ctx.message.server
    print(bot.voice_clients)
    if bot.is_voice_connected(server):
        voice_client = bot.voice_client_in(server)
        try:
            asyncio.ensure_future(voice_client.disconnect())
        except Exception as e:
            return await bot.say(embed=error("Could not leave voice channel", str(e)))
    else:
        await bot.say(embed=error("Could not leave voice channel", "I am not connected to a voice channel!"))


@bot.command(pass_context=True)
async def l(ctx):
    return await leave(ctx)


@bot.command(pass_context=True)
async def dis(ctx):
    return await leave(ctx)


@bot.command(pass_context=True)
async def disconnect(ctx):
    return await leave(ctx)


@bot.command(pass_context=True)
async def fuckoff(ctx):
    return await leave(ctx)


bot.run(TOKEN)
