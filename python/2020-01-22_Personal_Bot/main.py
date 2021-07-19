import discord
from discord.ext import commands
import settings
import youtube_dl
import os
import wavelink
import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("127.0.0.1", 2333))

class Bot(commands.Bot):
    def __init__(self):
        super(Bot, self).__init__(command_prefix=["!"])

bot = Bot()

token = "[REDACTED]"
bot.run(token)