import discord
from discord.ext import commands
import praw
from settings import *
import os
import datetime
import sys

os.system("clear")

client = commands.Bot(command_prefix=prefix)
client.remove_command("help")

redditclient = praw.Reddit(client_id='[REDACTED]',
                           client_secret='[REDACTED]',
                           user_agent='[REDACTED]')

async def process_commands(message):
    content = message.content
    if content.startswith(prefix + "reddit "):
        await reddit(message)

@client.event
async def on_ready():
    print("[*] Ready")
    print(client.user.n)

@client.event
async def on_message(message):
    if message.author.id == "[REDACTED]":
        print("[*] Recieved message: " + message.content)
        await process_commands(message)

async def reddit(message):
    args = message.content.replace(prefix + "reddit ", "").split()
    subreddit = args[0]
    del args[0]
    nsfw = False
    sort = "hot"
    link = False
    for arg in args:
        if arg.lower().startswith("nsfw") and ":" in arg:
            _, value = arg.split(":")
            nsfw = (True if value.lower().strip() == 'true' else False)
        elif arg.lower().startswith("sort") and ":" in arg:
            _, value = arg.split(":")
            sort = (value if value.lower().strip() in ['hot', 'new', 'top', 'controversial', 'rising'] else "hot")
        elif arg.lower().startswith("link") and ":" in arg:
            _, value = arg.split(":")
            link = (True if value.lower().strip() == 'true' else False)
        else:
            pass
    try:
        sub = redditclient.subreddit(subreddit)
    except:
        try:
            sub = redditclient.redditor(subreddit)
        except:
            return await message.edit(content="Subreddit/user not found")
    



token = "[REDACTED]"

try:
    client.loop.run_until_complete(client.start(token, bot=False))
except KeyboardInterrupt:
    print("[*] Closing Cyborg...")
    client.loop.run_until_complete(client.logout())
finally:
    client.loop.close()
    sys.exit(0)