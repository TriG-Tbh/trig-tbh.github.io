# DNI

import random
import discord
import datetime
import asyncio

import cogs.settings as settings

async def confirmation(bot, ctx):
    values = [c for c in "0123456789"]
    code = ""
    for _ in range(4):
        code += random.choice(values)

    def check(message):
        return (
            message.content == code
            or message.content.lower().strip().lstrip() == "cancel"
        ) and message.channel == ctx.message.channel and message.author == ctx.message.author

    embed = botembed(
        "Confirm",
        "Are you sure you want to proceed? Type `{}` to proceed, or `cancel` to cancel."
        .format(code), settings.BLUE)
    await ctx.send(embed=embed)
    try:
        confirm = await bot.wait_for("message", check=check, timeout=60.0)
    except asyncio.TimeoutError:
        embed = botembed("Confirmation Failed",
                         "Confirmation failed. Please run command again.", settings.RED)
        await ctx.send(embed=embed)
        return False
    else:
        if confirm.content.lower().strip().lstrip() == "cancel":
            embed = botembed("Confirmation Failed",
                             "Confirmation failed. Please run command again.",
                             settings.RED)
            await ctx.send(embed=embed)
            return False
        return True

def botembed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.timestamp = datetime.datetime.utcnow()
    return embed