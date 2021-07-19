import discord
from discord.ext import commands

import praw
import random
import io
import aiohttp

import requests

import os

os.system('clear')

prefix = "."

bot = commands.Bot(command_prefix=prefix)
bot.remove_command("help")

redditclient = praw.Reddit(client_id='[REDACTED]',
                           client_secret='[REDACTED]',
                           user_agent='[REDACTED]')


@bot.event
async def on_ready():
    print("Ready")


@bot.command()
async def reddit(ctx, subreddit=None, mode=None):
    if subreddit is None:
        return await ctx.send("Please specify a subreddit")
    try:
        subreddit = redditclient.subreddit(subreddit)
    except:
        return await ctx.send("Unknown subreddit. Please check the subreddit name or the usage of the command")
    posts = []
    if mode is None:
        for post in subreddit.hot(limit=100):
            posts.append(post)
    else:
        if mode.lower().strip() == "hot":
            for post in subreddit.hot(limit=100):
                posts.append(post)
        elif mode.lower().strip() == "new":
            for post in subreddit.new(limit=100):
                posts.append(post)
        else:
            for post in subreddit.hot(limit=100):
                posts.append(post)
    nsfw = True
    while nsfw:
        post = random.choice(posts)
        nsfw = post.over_18
        if not nsfw:
            text = post.is_self
            if not text:
                break
    url = post.url
    permalink = "https://www.reddit.com" + post.permalink
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.message.channel.send('Could not download file')
                data = io.BytesIO(await resp.read())
                #await ctx.send(url + " (If the post was incorrectly labeled as SFW, visit the link to report it)", file=discord.File(data, 'image0.png'))
                await ctx.send(permalink + " (If the post was incorrectly labeled as SFW, visit the link to report it)", file=discord.File(data, 'image0.png'))

@bot.command()
async def addemoji(ctx, name=None, url=None):
    goahead = False
    for role in ctx.message.author.roles:
        if role.name == "Administrator":
            goahead = True
            break
    if not goahead:
        return await ctx.send("You do not have permission to run this command")
    if name is None:
        return await ctx.send("Please specify a name")
    if url is None:
        return await ctx.send("Please specify an image URL")
    try:
        resp = requests.get(url)
        image = resp.content
        await ctx.guild.create_custom_emoji(name=name, image=image)
    except Exception as e:
        await ctx.send("Error creating emoji: " + str(e))
    else:
        await ctx.send("Successfully create :" + str(name) + ":")


@bot.command()
async def furry(ctx, target=None, mode=None):
    if target is not None:
        target = target.replace("<@", "")
        target = target.replace("<@!", "")
        target = target.replace(">", "")
        try:
            target = int(target)
        except:
            return await ctx.send("Invalid target")
        else:
            try:
                user = await bot.fetch_user(target)
            except:
                return await ctx.send("Cannot find member")
            member = discord.utils.find(lambda u: u.id == user.id, ctx.channel.guild.members)
            if member is None:
                return await ctx.send("Cannot find member")
            else:
                can = False
                for role in member.roles:
                    if role.name == "DM Spam":
                        can = True
                        break
                if not can:
                    return await ctx.send("User has disabled DM spam")
    else:
        user = await bot.fetch_user(ctx.message.author.id)
    dm = await user.create_dm()
    subreddit = redditclient.subreddit("furry")
    posts = []
    if mode is None:
        for post in subreddit.hot(limit=100):
            posts.append(post)
    else:
        if mode.lower().strip() == "hot":
            for post in subreddit.hot(limit=100):
                posts.append(post)
        elif mode.lower().strip() == "new":
            for post in subreddit.new(limit=100):
                posts.append(post)
        else:
            for post in subreddit.hot(limit=100):
                posts.append(post)
    nsfw = True
    while nsfw:
        post = random.choice(posts)
        nsfw = post.over_18
        if not nsfw:
            text = post.is_self
            if not text:
                break
    url = post.url
    permalink = "https://www.reddit.com" + post.permalink
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    return await ctx.message.channel.send('Could not download file')
                data = io.BytesIO(await resp.read())
                #await dm.send(url + " (If the post was incorrectly labeled as SFW, visit the link to report it)", file=discord.File(data, 'image0.png'))
                await ctx.send("You have been DMed a picture >:)")
                await dm.send(permalink + " (If the post was incorrectly labeled as SFW, visit the link to report it)", file=discord.File(data, 'image0.png'))

@bot.command()
async def help(ctx):
    with open("help.txt", "r") as help:
        await ctx.send("```" + help.read() + "```")


@bot.command()
async def hug(ctx, user=None):
    if user is None:
        return await ctx.send("Please specify a user")
    target = user.replace("<@", "")
    target = target.replace("<@!", "")
    target = target.replace(">", "")
    try:
        target = int(target)
    except:
        return await ctx.send("Invalid target")
    try:
        user = await bot.fetch_user(target)
    except:
        return await ctx.send("Cannot find member")
    await ctx.send("<@" + str(ctx.message.author.id) + "> has given <@" + str(target) + "> a hug!")


@bot.command()
async def slap(ctx, user=None):
    if user is None:
        return await ctx.send("Please specify a user")
    target = user.replace("<@", "")
    target = target.replace("<@!", "")
    target = target.replace(">", "")
    try:
        target = int(target)
    except:
        return await ctx.send("Invalid target")
    try:
        user = await bot.fetch_user(target)
    except:
        return await ctx.send("Cannot find member")
    await ctx.send("Ouch, <@" + str(ctx.message.author.id) + "> has slapped <@" + str(target) + ">!")


@bot.command()
async def rps(ctx, move=None):
    if move is None:
        return await ctx.send("Move not specified")
    async with ctx.typing():
        move = move.lower().strip()
        moves = ['rock', 'paper', 'scissors']
        if move not in moves:
            return await ctx.send("Invalid move - use `.help` to view valid moves")
        botmove = random.choice(moves)
        win = ""
        if move == "rock" and botmove == "scissors":
            win = True
        elif move == "scissors" and botmove == "paper":
            win = True
        elif move == "paper" and botmove == "rock":
            win = True
        elif botmove == "rock" and move == "scissors":
            win = False
        elif botmove == "scissors" and move == "paper":
            win = False
        elif botmove == "paper" and move == "rock":
            win = False
        elif botmove == move:
            win = None

    if win is None:
        await ctx.send("I chose **" + botmove + "**! We tied!")
    elif win:
        await ctx.send("I chose **" + botmove + "**! You won!")
    else:
        await ctx.send("I chose **" + botmove + "**! I won!")


@bot.command()
async def kick(ctx, user=None):
    goahead = False
    for role in ctx.message.author.roles:
        if role.name == "Administrator":
            goahead = True
            break
    if not goahead:
        return await ctx.send("You do not have permission to run this command")
    if user is None:
        return await ctx.send("Please specify a user")
    target = user.replace("<@", "")
    target = target.replace("<@!", "")
    target = target.replace(">", "")
    try:
        target = int(target)
    except:
        return await ctx.send("Invalid target")
    try:
        user = await bot.fetch_user(target)
    except:
        return await ctx.send("Cannot find member")
    name = user.name
    try:
        await ctx.channel.guild.kick(user)
    except:
        return await ctx.send("User cannot be kicked")
    await ctx.send("User " + str(name) + " has been kicked")


@bot.command()
async def ban(ctx, user=None):
    goahead = False
    for role in ctx.message.author.roles:
        if role.name == "Administrator":
            goahead = True
            break
    if not goahead:
        return await ctx.send("You do not have permission to run this command")
    if user is None:
        return await ctx.send("Please specify a user")
    target = user.replace("<@", "")
    target = target.replace("<@!", "")
    target = target.replace(">", "")
    try:
        target = int(target)
    except:
        return await ctx.send("Invalid target")
    try:
        user = await bot.fetch_user(target)
    except:
        return await ctx.send("Cannot find member")
    name = user.name
    try:
        await ctx.channel.guild.ban(user)
    except:
        return await ctx.send("User cannot be banned")
    await ctx.send("User " + str(name) + " has been banned")


@bot.command()
async def clear(ctx, number=None):
    if ctx.channel.type != discord.ChannelType.private:
        goahead = False
        for role in ctx.message.author.roles:
            if role.name == "Administrator":
                goahead = True
                break
        if not goahead:
            return await ctx.send("You do not have permission to run this command")
    if number is None:
        return await ctx.send(
            "Please specify the number of messages you want to clear (use \".help\" for valid inputs)")
    mgs = []
    if number.lower().strip() == "all":
        number = None
    else:
        try:
            number = int(number)
        except:
            return await ctx.send("Invalid number of messages")
        else:
            if number < 1:
                return await ctx.send("Please specify a larger number")
            number += 1
    if ctx.channel.type != discord.ChannelType.private:
        async for x in ctx.message.channel.history(limit=number):
            mgs.append(x)
    else:
        number -= 1
        n = 0
        mgs = await ctx.message.channel.history().flatten()
        for message in mgs:
            if n == number:
                break
            if message.author.name == bot.user.name:
                await message.delete()
                n += 1
        number += 1
    if ctx.channel.type == discord.ChannelType.private:
        pass
    else:
        await ctx.message.channel.delete_messages(mgs)
    user = await bot.fetch_user(ctx.message.author.id)
    dm = await user.create_dm()
    aoran = ""
    if number - 1 > 1:
        aoran = "s were"
    else:
        aoran = " was"

    await dm.send(str(number - 1) + " message" + aoran + " cleared from <#" + str(ctx.message.channel.id) + ">")

@bot.command()
async def kill(ctx):
    await ctx.send("Killing, please wait...")
    await bot.change_presence(status=discord.Status.offline)
    if ctx.message.author.name != "TriG":
        return await ctx.send("You are not allowed to use this command")
    for i in range(3):
        import sys
        sys.exit("Remotely killed")


TOKEN = "[REDACTED]"

bot.run(TOKEN)
