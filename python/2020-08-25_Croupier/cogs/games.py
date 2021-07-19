import discord
from discord.ext import commands
import cogs.functions as functions

def botembed(description):
    embed = functions.embed("🎲 Games")
    embed.description = description
    return embed

class GameManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


def setup(bot):
    bot.add_cog(GameManager(bot))