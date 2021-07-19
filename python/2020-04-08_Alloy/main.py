import settings
import datetime
import asyncio

import discord
from discord.ext import commands

global bot
bot = commands.Bot(command_prefix=settings.PREFIX)

def is_offline():
    server = bot.get_guild("[REDACTED]")
    dyno = discord.utils.find(lambda m: m.id == "[REDACTED]", server.members)
    if str(dyno.status) == "offline":
        return True
    return False

red = 0xff470f
blue = 0x117ea6
green = 0x23d160

    
def botembed(title, description, color):
    embed = discord.Embed(title=title, description=description, color=color)
    embed.timestamp = datetime.datetime.utcnow()
    return embed

    

@bot.event
async def on_ready():
    print("Ready")
    

@bot.event
async def on_raw_message_delete(payload):
    if is_offline():
        channel = bot.get_channel("[REDACTED]")
        if payload.cached_message is None:
            embed = botembed("", "**Message deleted in** <#{}>".format(payload.channel_id), red)
            embed.add_field(name="Content", value="?")
            embed.set_footer(text="Message ID: {}".format(payload.message_id))
            await channel.send(embed=embed)
        else:
            message = payload.cached_message
            embed = botembed("", "**Message sent by** <@{}> **deleted in** <#{}>".format(message.author.id, message.channel.id), red)
            embed.set_author(name="{}#{}".format(message.author.name, message.author.discriminator), icon_url=str(message.author.avatar_url_as(static_format="png", size=1024)))
            if message.content != "":
                embed.add_field(name="Content", value=message.content)
            if len(message.attachments) != 0:
                embed.add_field(name="Attachments", value=", \n".join(a.url for a in message.attachments))
            embed.set_footer(text="Author ID: {} | Message ID: {}".format(message.author.id, message.id))
            await channel.send(embed=embed)

@bot.event
async def on_message_edit(before, after):
    if is_offline():
        channel = bot.get_channel("[REDACTED]")
        before_content = before.content
        after_content = after.content
        if before_content != after_content:
            embed = botembed("", "**Message edited in** <#{}> [Jump to Message]({})".format(before.channel.id, before.jump_url), blue)
            embed.set_author(name="{}#{}".format(before.author.name, before.author.discriminator), icon_url=str(before.author.avatar_url_as(static_format="png", size=1024)))

            embed.add_field(name="Before", value=before_content, inline=False)
            embed.add_field(name="After", value=after_content, inline=False)
            embed.set_footer(text="Author ID: {} | Message ID: {}".format(before.author.id, before.id))
            await channel.send(embed=embed)



@bot.event
async def on_member_update(before, after):
    if str(before.status) != str(after.status):
        if before.bot:
            channel = bot.get_channel("[REDACTED]")
            if str(after.status) == "offline":
                embed = botembed("", "<@{}> has gone offline".format(before.id), red)
                embed.set_author(name="{}#{}".format(before.name, before.discriminator), icon_url=str(before.avatar_url_as(static_format="png", size=1024)))
                embed.set_footer(text="ID: {}".format(before.id))
            elif str(after.status) == "online":
                embed = botembed("", "<@{}> has come online".format(before.id), green)
                embed.set_author(name="{}#{}".format(before.name, before.discriminator), icon_url=str(before.avatar_url_as(static_format="png", size=1024)))
                embed.set_footer(text="ID: {}".format(before.id))
            await channel.send(embed=embed)

    if is_offline():
        channel = bot.get_channel("[REDACTED]")
        roles_before = before.roles
        roles_after = after.roles
        different = list(set(roles_before) ^ set(roles_after))
        if len(different) == 0:
            return
        role = different[0]
        if role in list(roles_before):
            embed = botembed("", "<@{}> was removed from the `{}` role".format(before.id, role.name), blue)
            embed.set_author(name="{}#{}".format(before.name, before.discriminator), icon_url=str(before.avatar_url_as(static_format="png", size=1024)))
            embed.set_footer(text="ID: {}".format(before.author.id))
            await channel.send(embed=embed)
        elif role in list(roles_after):
            embed = botembed("", "<@{}> was given the `{}` role".format(before.id, role.name), blue)
            embed.set_author(name="{}#{}".format(before.name, before.discriminator), icon_url=str(before.avatar_url_as(static_format="png", size=1024)))
            embed.set_footer(text="ID: {}".format(before.author.id))
            await channel.send(embed=embed)

@bot.event
async def on_guild_channel_create(channel):
    if True:
        log = bot.get_channel("[REDACTED]")
        embed = botembed("", "**Channel created: <#{}>**".format(channel.id), green)
        embed.set_author(name=channel.guild.name, icon_url=str(channel.guild.icon_url))
        embed.set_footer(text="ID: {}".format(channel.id))
        await log.send(embed=embed)

@bot.event
async def on_guild_channel_delete(channel):
    if True:
        log = bot.get_channel("[REDACTED]")
        embed = botembed("", "**Channel deleted: #{}**".format(channel.name), red)
        embed.set_author(name=channel.guild.name, icon_url=str(channel.guild.icon_url))
        embed.set_footer(text="ID: {}".format(channel.id))
        await log.send(embed=embed)

@bot.event
async def on_member_remove(member):
    if is_offline():
        channel = bot.get_channel("[REDACTED]")
        async for log in member.guild.audit_logs(limit=100):
            if log.action == discord.AuditLogAction.kick and log.target.id == member:
                embed = botembed("", "<@{}> {}#{}".format(member.id, member.name, member.discriminator), red)
                embed.set_author(name="Member Kicked", icon_url=str(member.avatar_url_as(static_format="png", size=1024)))
                embed.set_footer(text="ID: {}".format(member.id))
                return await channel.send(embed=embed)
            elif log.action == discord.AuditLogAction.ban and log.target.id == member:
                embed = botembed("", "<@{}> {}#{}".format(member.id, member.name, member.discriminator), red)
                embed.set_author(name="Member Banned", icon_url=str(member.avatar_url_as(static_format="png", size=1024)))
                embed.set_footer(text="ID: {}".format(member.id))
                return await channel.send(embed=embed)
            embed = botembed("", "<@{}> {}#{}".format(member.id, member.name, member.discriminator), red)
            embed.set_author(name="Member Left", icon_url=str(member.avatar_url_as(static_format="png", size=1024)))
            embed.set_footer(text="ID: {}".format(member.id))
            await channel.send(embed=embed)

@bot.command()
async def status(ctx):
    bots = [m for m in ctx.guild.members if m.bot]
    message = ""
    for bot in bots:
        message += "<@{}>: **{}**\n".format(bot.id, str(bot.status).title())
    embed = botembed("", message, blue)
    embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon_url))
    await ctx.send(embed=embed)
    


token = settings.TOKEN
bot.run(token)