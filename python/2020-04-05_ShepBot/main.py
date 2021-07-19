import settings

import asyncio
import multiprocessing
import random
import re
import os
import requests
import praw
import io
import aiohttp

import discord
from discord.ext import commands


bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command("help")

reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')


async def send_message(bot, predefined=None, channel=None):
    messages = ["person above mega gay", "TriG good at art", "https://cdn.discordapp.com/attachments/621100618748002364/696325997653524509/image0.png",
                "nominate [REDACTED] for best artist", "shepbot for president"]
    if channel is None:
        channel = bot.get_channel("[REDACTED]")
    else:
        channel = bot.get_channel(channel)
    if predefined is None:
        message = random.choice(messages)
    else:
        message = predefined
    await channel.send(message)


@bot.event
async def on_member_join(member):
    channel = bot.get_channel("[REDACTED]")
    await channel.send("Welcome **<@{}>** to the Secret Headquarters for Epic Puppies! :wave:".format(member.id))


@bot.event
async def on_member_remove(member):
    async for log in member.guild.audit_logs(limit=100):
        if log.action == discord.AuditLogAction.kick and log.target.id == member:
            return
        elif log.action == discord.AuditLogAction.ban and log.target.id == member:
            return
    channel = bot.get_channel("[REDACTED]")
    await channel.send("So sad to see you go, {}#{} :wave:".format(member.name, member.discriminator))


@bot.event
async def on_raw_reaction_add(payload):
    if payload.user_id == bot.user.id:
        return

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    member = payload.member
    if message.id == "[REDACTED]":
        role = discord.utils.find(
            lambda r: r.id == "[REDACTED]", member.guild.roles)
        await member.add_roles(role)
    if message.id == "[REDACTED]":
        role = discord.utils.find(
            lambda r: r.id == "[REDACTED]", member.guild.roles)
        await member.add_roles(role)


async def puppy(bot):
    channel = bot.get_channel("[REDACTED]")
    link = redditimg("rarepuppers")
    if link is not None:
        if "imgur" in link:
            await channel.send(link)
        else:
            extension = link.split("/")[-1].split(".")[1]
            async with aiohttp.ClientSession() as session:
                async with session.get(link) as resp:
                    if resp.status != 200:
                        pass
                    data = io.BytesIO(await resp.read())
                    try:
                        await channel.send(file=discord.File(data, 'puppy.{}'.format(extension)))
                    except discord.errors.HTTPException:
                        pass


@bot.event
async def on_ready():
    print("Ready")
    while True:
        await asyncio.sleep(1800)
        await puppy(bot)
        await asyncio.sleep(1800)
        await send_message(bot, predefined="shepbot is love, shepbot is life")
        await asyncio.sleep(1800)
        await puppy(bot)
        await asyncio.sleep(1800)
        pass


def redditimg(subname):
    subreddit = reddit.subreddit(subname)
    try:
        for _ in subreddit.new(limit=1):
            pass
    except:
        return None

    posts = []
    i = 1
    for post in subreddit.hot(limit=None):
        if i > 50:
            break
        if not post.over_18:
            if not post.is_self:
                posts.append(post)
        i += 1
    if len(posts) < 1:
        return None
    keep_choosing = True
    blacklist = []
    while keep_choosing:
        post = random.choice(posts)
        if post in blacklist:
            goodposts = [p for p in posts if not p.over_18]
            if len(goodposts) == 0:
                return None
            continue
        if not post.over_18:
            link = post.url
            if link.endswith(".png") or link.endswith(".jpg") or link.endswith(".jpeg") or "imgur" in link:
                keep_choosing = False
                break
        blacklist.append(post)
    return post.url


@bot.event
async def on_message(message):
    if not message.channel.type == discord.ChannelType.private:
        if "shepbot is love, shepbot is life" in message.content.lower() and message.author.id != bot.user.id:
            await message.channel.send("shepbot is love, shepbot is life")
        if "shepbot sucks" in message.content.lower():
            base = os.path.dirname(os.path.realpath(__file__))
            lpath = os.path.join(base, "wtf.txt")
            with open(lpath) as f:
                text = f.read()
            await message.channel.send(text)
        if "cheese" in message.content.lower() or "sergal" in message.content.lower():
            await message.channel.send("merp")
        if "not funny" in message.content.lower():
            await message.channel.send("didn't laugh")
        elif "funny" in message.content.lower():
            await message.channel.send("laughed")
        if "guess what" in message.content.lower():
            await message.channel.send("nobody asked")
        if len(message.mentions) > 0 and message.author.id != bot.user.id:
            if "[REDACTED]" not in [role.id for role in message.author.roles]:
                await message.channel.send("<@{}> no u".format(message.author.id))
        await bot.process_commands(message)
    else:
        if message.author.id not in ["[REDACTED]", "[REDACTED]"]:
            return
        else:
            channel = bot.get_channel("[REDACTED]")
            await channel.send(message.content)


@bot.command()
async def randomemoji(ctx):
    emoji = random.choice(ctx.guild.emojis)
    await ctx.send("<:{}:{}>".format(emoji.name, emoji.id))


@bot.command()
async def count(ctx, *word):
    if len(word) == 0:
        return await ctx.send("You need to specify a message to look for!")
    word = " ".join(word)
    messages = await ctx.channel.history(limit=10000).flatten()
    # print('here')
    mcount = len(messages)
    messagetosend = ""
    if mcount >= 1:
        messagetosend += "Messages scanned: **{}**\n".format(mcount)
        usermessages = [m for m in messages if m.author.id ==
                        ctx.message.author.id]
        ucount = len(usermessages)
        if ucount >= 1:
            messagetosend += "Messages sent by user: **{}**\n".format(ucount)
            bruhmessages = [
                m for m in usermessages if word in m.content.lower()]
            bcount = len(bruhmessages)
            messagetosend += "Amount of times \"{}\" appears in user messages: **{}**".format(
                word, bcount)
    if messagetosend != "":
        await ctx.send(messagetosend)


@bot.command()
async def randommessage(ctx):
    await send_message(bot)


@bot.command()
async def applyall(ctx, roleid):
    role = discord.utils.find(lambda r: r.id == role.id, ctx.guild.roles)
    for member in ctx.guild.members:
        await member.add_roles(role)

# @bot.command()
# async def invite(ctx):
#    await ctx.send("Want to invite this bot into your server (idk why you would)? Visit https://discordapp.com/api/oauth2/authorize?client_id=[REDACTED]&permissions=8&scope=bot")


@bot.command()
async def airstrike(ctx, member: discord.Member = None):
    if member is None:
        return await ctx.send("You need to specify a user to airstrike!")
    try:
        await ctx.send(":boom: KABOOM! <@{}> has been hit by an airstrike!".format(member.id))
    except:
        await ctx.send("Please specify a user to airstrike.")


@bot.command()
async def fnaf(ctx):
    goahead = False
    for role in ctx.message.author.roles:
        if role.id in ["[REDACTED]", "[REDACTED]", "[REDACTED]"]:
            goahead = True
    if not goahead:
        return
    base = os.path.dirname(os.path.realpath(__file__))
    lpath = os.path.join(base, "fnaf.txt")
    with open(lpath) as f:
        lyrics = f.read()
    n = 2000
    chunks = [lyrics[i:i+n] for i in range(0, len(lyrics), n)]
    for chunk in chunks:
        await ctx.send(chunk)


@bot.command()
async def despacito(ctx):
    goahead = False
    for role in ctx.message.author.roles:
        if role.id in ["[REDACTED]", "[REDACTED]", "[REDACTED]"]:
            goahead = True
    if not goahead:
        return
    base = os.path.dirname(os.path.realpath(__file__))
    lpath = os.path.join(base, "lyrics.txt")
    with open(lpath) as f:
        lyrics = f.read()
    n = 2000
    chunks = [lyrics[i:i+n] for i in range(0, len(lyrics), n)]
    for chunk in chunks:
        await ctx.send(chunk)


@bot.command()
async def emoji(ctx, name=None, url=None):
    if ctx.message.author.id not in ["[REDACTED]", "[REDACTED]"]:
        return
    if name is None:
        return await ctx.send("Please specify a name for the emoji.")
    if url is None:
        if len(ctx.message.attachments) < 1:
            return await ctx.send("Please specify an image for the emoji (valid image URL/attachment).")
        else:
            url = ctx.message.attachments[0].url
    try:
        resp = requests.get(url)
        image = resp.content
        await ctx.guild.create_custom_emoji(name=name, image=image)
    except Exception as e:
        await ctx.send("Error creating emoji: " + str(e))
    else:
        emoji = discord.utils.find(lambda e: e.name == name, ctx.guild.emojis)
        await ctx.send("Successfully created <:" + str(name) + ":{}>".format(emoji.id))


@bot.command()
async def help(ctx):
    message = """.count <string>: searches the current channel for all of the times a message that contains a specific phrase has been sent by the command user
.randommessage: will send a random message in the general channel
.airstrike <user>: Hits a user with an airstrike
.despacito (can only be used by staff): sends the lyrics to Despacito
"""
    await ctx.send(message)


bot.run(settings.TOKEN)
