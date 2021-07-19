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
    botembed = embed("Error", color=0xff0000)
    botembed.description = errormsg
    return botembed


def isowner(user):
    return user.id == "[REDACTED]"

# def isadmin()
