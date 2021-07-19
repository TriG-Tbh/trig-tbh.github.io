import discord
from discord.ext import commands
import os
import importlib
import sys
import random


blacklist = ["settings", "functions"]

starboardrequired = 3

path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(path, "cogs"))

import cogs.settings as settings
import cogs.functions as functions

bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command("help")

def starboardembed():
    embed = functions.embed("Starboard", color=0xffff50)
    return embed

def auditlogembed():
    embed = functions.embed("Audit Log", color=0x72bcd4)
    return embed

def roleembed(name):
    embed = functions.embed("Role Menu - {}".format(name), color=0x00008b)
    return embed

@bot.event
async def on_member_join(member):
    embed = functions.embed("System", color=0x0000ff)
    quote = []
    words = ["boop", "beep", "bop"]
    for _ in range(random.randint(2, 4)):
        quote.append(random.choice(words))
    quote[0] = quote[0].title()
    quote = " ".join(quote)
    aoran = ""
    if member.bot:
        aoran = "robot"
    else:
        aoran = "human"
    embed.add_field(name="New Member", value="{}. A new {} has joined the server. Please welcome <@{}>!".format(quote, aoran, member.id), inline=False)
    embed.set_thumbnail(url=str(member.avatar_url_as(static_format="png", size=1024)))
    channel = bot.get_channel("[REDACTED]")
    await channel.send(embed=embed)
    role = [r for r in member.guild.roles if r.id == "[REDACTED]"][0]
    await member.add_roles(role)
    embed = auditlogembed()
    embed.set_thumbnail(url=str(member.avatar_url_as(static_format="png", size=1024)))
    embed.add_field(name="Member Joined", value="<@{}> {}#{}".format(member.id, member.name, member.discriminator), inline=False)
    channel = bot.get_channel("[REDACTED]")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    async for log in member.guild.audit_logs(limit=100):
        if log.action == discord.AuditLogAction.kick and log.target.id == member:
            embed = auditlogembed()
            embed.set_thumbnail(url=str(member.avatar_url_as(static_format="png", size=1024)))
            embed.add_field(name="Member Kicked", value="<@{}> {}#{}".format(member.id, member.name, member.discriminator), inline=False)
            channel = bot.get_channel("[REDACTED]")
            return await channel.send(embed=embed)
        elif log.action == discord.AuditLogAction.ban and log.target.id == member:
            embed = auditlogembed()
            embed.set_thumbnail(url=str(member.avatar_url_as(static_format="png", size=1024)))
            embed.add_field(name="Member Banned", value="<@{}> {}#{}".format(member.id, member.name, member.discriminator), inline=False)
            channel = bot.get_channel("[REDACTED]")
            return await channel.send(embed=embed)
    embed = auditlogembed()
    embed.set_thumbnail(url=str(member.avatar_url_as(static_format="png", size=1024)))
    embed.add_field(name="Member Left", value="<@{}> {}#{}".format(member.id, member.name, member.discriminator), inline=False)
    channel = bot.get_channel("[REDACTED]")
    return await channel.send(embed=embed)
    
@bot.command()
async def roles(ctx):
    channel = bot.get_channel("[REDACTED]")
    embed = roleembed("Hobbies")
    embed.add_field(name="test", value=":regional_indicator_a:")
    await channel.send(embed=embed)

@bot.command()
async def test(ctx):
    await on_member_remove(ctx.message.author)


@bot.event
async def on_raw_reaction_add(payload):
    emoji = payload.emoji
    server = discord.utils.find(lambda s: s.id == "[REDACTED]", bot.guilds)
    channel = discord.utils.find(lambda c: c.id == payload.channel_id, server.channels)
    if emoji.name == "⭐":
        message = await channel.fetch_message(payload.message_id)
        if message.channel.is_nsfw():
            return
        reactioncount = [r for r in message.reactions if r.emoji == "⭐"][0].count
        required = starboardrequired
        if reactioncount == required:
            text = "🌠 {} | ID: {} | <#{}>".format(reactioncount, message.id, message.channel.id)
            embed = starboardembed()
            embed.add_field(name="Author", value="<@{}>".format(message.author.id), inline=False)
            if message.content != "":
                embed.add_field(name="Message", value=message.content, inline=False)
            if len(message.attachments) != 0:
                embed.set_image(url=message.attachments[0].url)
            embed.add_field(name="Link", value="[Jump to Message]({})".format(message.jump_url), inline=False)
            channel = discord.utils.find(lambda c: c.id == "[REDACTED]", server.channels)
            await channel.send(text, embed=embed)
        elif reactioncount > required:
            channel = discord.utils.find(lambda c: c.id == "[REDACTED]", server.channels)
            messages = await channel.history(limit=None).flatten()
            sbmessage = discord.utils.find(lambda m: "ID: {}".format(message.id) in m.content, messages)
            text = "🌠 {} | ID: {} | <#{}>".format(reactioncount, message.id, message.channel.id)
            embed = starboardembed()
            embed.add_field(name="Author", value="<@{}>".format(message.author.id), inline=False)
            if message.content != "":
                embed.add_field(name="Message", value=message.content, inline=False)
            if len(message.attachments) != 0:
                embed.set_image(url=message.attachments[0].url)
            embed.add_field(name="Link", value="[Jump to Message]({})".format(message.jump_url), inline=False)
            await sbmessage.edit(content=text, embed=embed)

@bot.event
async def on_raw_reaction_remove(payload):
    emoji = payload.emoji
    server = discord.utils.find(lambda s: s.id == "[REDACTED]", bot.guilds)
    channel = discord.utils.find(lambda c: c.id == payload.channel_id, server.channels)
    if emoji.name == "⭐":
        message = await channel.fetch_message(payload.message_id)
        try:
            reactioncount = [r for r in message.reactions if r.emoji == "⭐"][0].count
        except IndexError:
            channel = discord.utils.find(lambda c: c.id == "[REDACTED]", server.channels)
            messages = await channel.history(limit=None).flatten()
            sbmessage = discord.utils.find(lambda m: "ID: {}".format(message.id) in m.content, messages)
            try:
                return await sbmessage.delete()
            except:
                return
        required = starboardrequired
        if reactioncount >= required:
            channel = discord.utils.find(lambda c: c.id == "[REDACTED]", server.channels)
            messages = await channel.history(limit=None).flatten()
            sbmessage = discord.utils.find(lambda m: "ID: {}".format(message.id) in m.content, messages)
            text = "🌠 {} | ID: {} | <#{}>".format(reactioncount, message.id, message.channel.id)
            embed = starboardembed()
            embed.add_field(name="Author", value="<@{}>".format(message.author.id), inline=False)
            if message.content != "":
                embed.add_field(name="Message", value=message.content, inline=False)
            if len(message.attachments) != 0:
                embed.set_image(url=message.attachments[0].url)
            embed.add_field(name="Link", value="[Jump to Message]({})".format(message.jump_url), inline=False)
            await sbmessage.edit(content=text, embed=embed)
        else:
            channel = discord.utils.find(lambda c: c.id == "[REDACTED]", server.channels)
            messages = await channel.history(limit=None).flatten()
            sbmessage = discord.utils.find(lambda m: "ID: {}".format(message.id) in m.content, messages)
            await sbmessage.delete()

@bot.event
async def on_raw_message_delete(payload):
    channel = bot.get_channel("[REDACTED]")
    if payload.cached_message is None:
        embed = auditlogembed()
        embed.add_field(name="Message Deleted", value="Unknown message deleted in <#{}> (ID: {})".format(payload.channel_id, payload.message_id), inline=False)
        await channel.send(embed=embed)
    else:
        message = payload.cached_message
        embed = auditlogembed()
        embed.add_field(name="Message Deleted", value="Message sent by <@{}> deleted in <#{}>".format(message.author.id, message.channel.id), inline=False)
        if message.content != "":
            embed.add_field(name="Content", value=message.content, inline=False)
        if len(message.attachments) != 0:
            embed.add_field(name="Attachments", value="\n".join(a.url for a in message.attachments), inline=False)

        await channel.send(embed=embed)

@bot.event
async def on_raw_bulk_message_delete(payload):
    channel = bot.get_channel("[REDACTED]")
    if payload.cached_messages is None:
        embed = auditlogembed()
        embed.add_field(name="Messages Deleted", value="Unknown number of messages deleted in <#{}>".format(payload.channel_id), inline=False)
        await channel.send(embed=embed)
    else:
        embed = auditlogembed()
        embed.add_field(name="Message Deleted", value="{} messages deleted in <#{}>".format(len(payload.cached_messages), payload.channel_id), inline=False)
        await channel.send(embed=embed)

@bot.event
async def on_member_update(before, after):
    channel = bot.get_channel("[REDACTED]")
    roles_before = before.roles
    roles_after = after.roles
    different = list(set(roles_before) ^ set(roles_after))
    if len(different) == 0:
        return
    role = different[0]
    if role in list(roles_before):
        embed = auditlogembed()
        embed.set_thumbnail(url=str(before.avatar_url_as(static_format="png", size=1024)))
        embed.add_field(name="Role Removed", value="<@{}> was removed from the `{}` role".format(before.id, role.name), inline=False)
        await channel.send(embed=embed)
    elif role in list(roles_after):
        embed = auditlogembed()
        embed.set_thumbnail(url=str(after.avatar_url_as(static_format="png", size=1024)))
        embed.add_field(name="Role Added", value="<@{}> was given the `{}` role".format(before.id, role.name), inline=False)
        await channel.send(embed=embed)
    

@bot.event
async def on_message_edit(before, after):
    channel = bot.get_channel("[REDACTED]")
    before_content = before.content
    after_content = after.content
    if before_content != after_content:
        embed = auditlogembed()
        embed.set_thumbnail(url=str(before.author.avatar_url_as(static_format="png", size=1024)))
        embed.add_field(name="Message Edited", value="Message sent by <@{}> edited".format(before.author.id), inline=False)
        embed.add_field(name="Before", value="`{}`".format(before_content), inline=False)
        embed.add_field(name="After", value="`{}`".format(after_content), inline=False)
        embed.add_field(name="Link", value="[Jump to Message]({})".format(before.jump_url), inline=False)
        await channel.send(embed=embed)



@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_message(message):
    if message.channel.type != discord.ChannelType.private:
        await bot.process_commands(message)


@bot.command()
async def verify(ctx):
    if "[REDACTED]" in [r.id for r in ctx.message.author.roles]:
        return
    new = [r for r in ctx.message.author.guild.roles if r.id == "[REDACTED]"][0]
    old = [r for r in ctx.message.author.guild.roles if r.id == "[REDACTED]"][0]
    await ctx.message.author.remove_roles(old)
    await ctx.message.author.add_roles(new)
    

for filename in os.listdir(f'{path}/cogs'):
    if filename.endswith(".py"):
        if filename[:-3] not in blacklist:
            bot.load_extension(f"cogs.{filename[:-3]}")

bot.run(settings.TOKEN)