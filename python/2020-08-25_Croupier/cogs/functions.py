# DNI

import discord
import random
import datetime


def embed(title, color=None):
    if color is None:
        color = random.randint(0, 0xffffff)
    botembed = discord.Embed(title=title, color=color)
    timestamp = datetime.datetime.utcnow()
    botembed.timestamp = timestamp
    return botembed


def error(errormsg):
    botembed = embed("❌ Error", color=0xff0000)
    botembed.description = errormsg
    return botembed


def isowner(user):
    return user.id == 424991711564136448

def humanize(td):
    seconds = int(td.total_seconds())
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = (seconds % 3600) % 60
    readable = []
    if h > 0:
        readable.append(f"{h} hours")
    if m > 0:
        readable.append(f"{m} minutes")
    if s > 0:
        readable.append(f"{s} seconds")
    
    formatted = ""
    if len(readable) > 1:
        formatted = ", ".join(readable[:-1]) + " and " + readable[-1]
    else:
        formatted = readable[0]
    return formatted