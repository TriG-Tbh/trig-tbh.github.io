# --- Local File Imports ---
from settings import *


# --- Environment Imports ---
import os
import sys
import random
import asyncio
import re
import urllib.request
import urllib.parse
from multiprocessing import Process


# --- Custom Imports ---
import discord
from discord.ext import commands
from discord.voice_client import VoiceClient
from discord import FFmpegPCMAudio
import youtube_dl
import pafy
#import ffprobe
import ffmpeg


# --- Global Declarations ---
global queue
queue = []


# --- Function Definitions ---

def error(message):
    embed = discord.Embed(title="Error Message", description=message, color=0xff0000)
    return embed

def success(message):
    embed = discord.Embed(title="Success Message", description=message, color=0x00ff00)
    return embed

def getstats(url):
    stats = {}
    video = pafy.new(url)
    stats["title"] = video.title
    stats["length"] = video.length
    return stats

def formatlen(seconds):
    minutes = seconds // 60
    seconds = seconds % 60
    seconds = str(round(seconds, 2))
    hours = int(minutes // 60)
    minutes = int(minutes % 60)
    if len(str(minutes)) == 1:
        minutes = "0" + str(minutes)
    if len(str(seconds).split('.')[0]) == 1:
        seconds = "0" + str(seconds)
    if len(str(hours)) == 1:
        hours = "0" + str(hours)
    time = ((hours + ":") if int(hours) > 0 else "") + minutes + ":" + seconds
    return time 


# --- Main Code ---

os.system("clear")
bot = commands.Bot(command_prefix=PREFIX)

@bot.event
async def on_ready():
    print("Ready.")

@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    if not channel:
        embed = error("You are not connected to a voice channel!")
        return await ctx.send(embed=embed)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    embed = success("Successfully joined {}!".format(channel))
    await ctx.send(embed=embed)
    async def connecttovcbase():
        voice = await channel.connect(reconnect=True)
    #newloop = asyncio.get_event_loop()
        #asyncio.run(connecttovcbase())
    #newloop.run_until_complete(connecttovcbase())
    asyncio.ensure_future(connecttovcbase())
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
    await voice.disconnect()
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        async def connecttovcbase():
            voice = await channel.connect(reconnect=True)
        asyncio.ensure_future(connecttovcbase())
        print("here")
    print("here")
    

@bot.command(pass_context=True, aliases=["dis", "fuckoff"])
async def disconnect(ctx):
    try:
        await bot.voice_clients[0].disconnect(force=True)
    except:
        embed = error("I am not connected to a voice channel!")
        return await ctx.send(embed=embed)
    else:
        embed = success("Successfully disconnected.")
        await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def hello(ctx):
    async with ctx.channel.typing():
        greetings = ["Hi!", "Hello!", "Good day!", "How do you do?", "Hello there."]
        greeting = random.choice(greetings)
    await ctx.send(greeting)


@bot.command(pass_context=True, aliases=['p'])
async def play(ctx):
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if voice is None:
        embed = error("I am not connected to a voice channel!")
        return await ctx.send(embed=embed)
    content = ctx.message.content
    if "http" in content:
        url = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\), ]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)
        url = url[0]
    else:
        if content.startswith(".p "):
            content = content[3:]
        elif content.startswith(".play "):
            content = content[6:]
        query = content
        query = query.replace(' ', '_')
        query_string = urllib.parse.urlencode({"search_query" : query})
        html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
        search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
        url = ("http://www.youtube.com/watch?v=" + search_results[0])
    song_exists = os.path.isfile("song.mp3")
    try:
        if song_exists:
            os.remove("song.mp3")
    except PermissionError:
        queue.append(url)
        embed = success("Song added to queue position {}".format(len(queue)))
        return await ctx.send(embed=embed)
    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    stats = getstats(url)
    time = formatlen(stats["length"])
    embed = success("Now playing: {} (`{}`)".format(stats["title"], time))
    print(voice.is_connected())
    source = discord.FFmpegPCMAudio("song.mp3")
    voice.play(source)
    voice.volume = 100
    print("hi")

token = "[REDACTED]"
try:
    bot.run(token)
except Exception as e:
    os.system("clear")
    print("Exception: " + str(e))
    print("Exiting...")
    sys.exit(1)