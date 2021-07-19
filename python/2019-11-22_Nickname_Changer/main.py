import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("ready")

@bot.command()
async def changeall(ctx, *nickname):
    if len(nickname) < 1:
        return
    nickname = " ".join(nickname)
    for member in ctx.channel.guild.members:
        try:
            await member.edit(nick=nickname)
        except:
            pass
    print("done")


token = "[REDACTED]"

bot.run(token)