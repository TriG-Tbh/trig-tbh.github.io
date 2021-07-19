import discord
from discord.ext import commands

import cogs.functions as functions
import cogs.settings as settings

class AuditLog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_offline(self):
        server = self.bot.get_guild("[REDACTED]")
        dyno = discord.utils.find(lambda m: m.id == "[REDACTED]",
                                server.members)
        if str(dyno.status) == "offline":
            return True
        return False

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.guild.id != "[REDACTED]":
            return
        if self.is_offline():
            log = self.bot.get_channel("[REDACTED]")
            embed = functions.botembed("", "**Channel created: <#{}>**".format(channel.id),
                            settings.GREEN)
            embed.set_author(name=channel.guild.name,
                            icon_url=str(channel.guild.icon_url))
            embed.set_footer(text="ID: {}".format(channel.id))
            await log.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        if channel.guild.id != "[REDACTED]":
            return
        if self.is_offline():
            log = self.bot.get_channel("[REDACTED]")
            embed = functions.botembed("", "**Channel deleted: #{}**".format(channel.name),
                            settings.RED)
            embed.set_author(name=channel.guild.name,
                            icon_url=str(channel.guild.icon_url))
            embed.set_footer(text="ID: {}".format(channel.id))
            await log.send(embed=embed)

    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id != "[REDACTED]":
            return
        if self.is_offline():
            channel = self.bot.get_channel("[REDACTED]")
            if payload.cached_message is None:
                embed = functions.botembed(
                    "", "**Message deleted in** <#{}>".format(payload.channel_id),
                    settings.RED)
                embed.add_field(name="Content", value="?")
                embed.set_footer(text="Message ID: {}".format(payload.message_id))
                await channel.send(embed=embed)
            else:
                message = payload.cached_message
                embed = functions.botembed(
                    "", "**Message sent by** <@{}> **deleted in** <#{}>".format(
                        message.author.id, message.channel.id), settings.RED)
                embed.set_author(name="{}#{}".format(message.author.name,
                                                    message.author.discriminator),
                                icon_url=str(
                                    message.author.avatar_url_as(
                                        static_format="png", size=1024)))
                if message.content != "":
                    embed.add_field(name="Content", value=message.content)
                if len(message.attachments) != 0:
                    embed.add_field(name="Attachments",
                                    value=", \n".join(
                                        a.url for a in message.attachments))
                embed.set_footer(text="Author ID: {} | Message ID: {}".format(
                    message.author.id, message.id))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        if member.guild.id != "[REDACTED]":
            return
        if self.is_offline():
            channel = self.bot.get_channel("[REDACTED]")
            async for log in member.guild.audit_logs(limit=100):
                if log.action == discord.AuditLogAction.kick and log.target.id == member:
                    embed = functions.botembed(
                        "", "<@{}> {}#{}".format(member.id, member.name,
                                                member.discriminator), settings.RED)
                    embed.set_author(name="Member Kicked",
                                    icon_url=str(
                                        member.avatar_url_as(static_format="png",
                                                            size=1024)))
                    embed.set_footer(text="ID: {}".format(member.id))
                    return await channel.send(embed=embed)
                elif log.action == discord.AuditLogAction.ban and log.target.id == member:
                    embed = functions.botembed(
                        "", "<@{}> {}#{}".format(member.id, member.name,
                                                member.discriminator), settings.RED)
                    embed.set_author(name="Member Banned",
                                    icon_url=str(
                                        member.avatar_url_as(static_format="png",
                                                            size=1024)))
                    embed.set_footer(text="ID: {}".format(member.id))
                    return await channel.send(embed=embed)
            embed = functions.botembed(
                "", "<@{}> {}#{}".format(member.id, member.name,
                                        member.discriminator), settings.RED)
            embed.set_author(name="Member Left",
                            icon_url=str(
                                member.avatar_url_as(static_format="png",
                                                    size=1024)))
            embed.set_footer(text="ID: {}".format(member.id))
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.guild.id != "[REDACTED]":
            return
        if str(before.status) != str(after.status):
            if before.bot:
                channel = self.bot.get_channel("[REDACTED]")
                if str(after.status) == "offline":
                    embed = functions.botembed("",
                                    "<@{}> has gone offline".format(before.id),
                                    settings.RED)
                    embed.set_author(name="{}#{}".format(before.name,
                                                        before.discriminator),
                                    icon_url=str(
                                        before.avatar_url_as(static_format="png",
                                                            size=1024)))
                    embed.set_footer(text="ID: {}".format(before.id))
                elif str(after.status) == "online":
                    embed = functions.botembed("", "<@{}> has come online".format(before.id),
                                    settings.GREEN)
                    embed.set_author(name="{}#{}".format(before.name,
                                                        before.discriminator),
                                    icon_url=str(
                                        before.avatar_url_as(static_format="png",
                                                            size=1024)))
                    embed.set_footer(text="ID: {}".format(before.id))
                await channel.send(embed=embed)

        if self.is_offline():
            channel = self.bot.get_channel("[REDACTED]")
            roles_before = before.roles
            roles_after = after.roles
            different = list(set(roles_before) ^ set(roles_after))
            if len(different) == 0:
                return
            role = different[0]
            if role in list(roles_before):
                embed = functions.botembed(
                    "", "<@{}> was removed from the `{}` role".format(
                        before.id, role.name), settings.BLUE)
                embed.set_author(name="{}#{}".format(before.name,
                                                    before.discriminator),
                                icon_url=str(
                                    before.avatar_url_as(static_format="png",
                                                        size=1024)))
                embed.set_footer(text="ID: {}".format(before.author.id))
                await channel.send(embed=embed)
            elif role in list(roles_after):
                embed = functions.botembed(
                    "",
                    "<@{}> was given the `{}` role".format(before.id,
                                                        role.name), settings.BLUE)
                embed.set_author(name="{}#{}".format(before.name,
                                                    before.discriminator),
                                icon_url=str(
                                    before.avatar_url_as(static_format="png",
                                                        size=1024)))
                embed.set_footer(text="ID: {}".format(before.author.id))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.guild.id != "[REDACTED]":
            return
        if self.is_offline() and not before.author.bot:
            channel = self.bot.get_channel("[REDACTED]")
            before_content = before.content
            after_content = after.content
            if before_content != after_content:
                embed = functions.botembed(
                    "", "**Message edited in** <#{}> [Jump to Message]({})".format(
                        before.channel.id, before.jump_url), settings.BLUE)
                embed.set_author(name="{}#{}".format(before.author.name,
                                                    before.author.discriminator),
                                icon_url=str(
                                    before.author.avatar_url_as(
                                        static_format="png", size=1024)))

                embed.add_field(name="Before", value=before_content, inline=False)
                embed.add_field(name="After", value=after_content, inline=False)
                embed.set_footer(text="Author ID: {} | Message ID: {}".format(
                    before.author.id, before.id))
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == "[REDACTED]":
            role = discord.utils.find(lambda r: r.id == "[REDACTED]",
                                    member.guild.roles)
            await member.add_roles(role)
    
    @commands.Cog.listener()
    async def on_raw_message_delete(self, payload):
        if payload.guild_id != "[REDACTED]":
            return
        if self.is_offline():
            channel = self.bot.get_channel("[REDACTED]")
            if payload.cached_message is None:
                embed = functions.botembed(
                    "", "**Message deleted in** <#{}>".format(payload.channel_id),
                    settings.RED)
                embed.add_field(name="Content", value="?")
                embed.set_footer(text="Message ID: {}".format(payload.message_id))
                await channel.send(embed=embed)
            else:
                message = payload.cached_message
                embed = functions.botembed(
                    "", "**Message sent by** <@{}> **deleted in** <#{}>".format(
                        message.author.id, message.channel.id), settings.RED)
                embed.set_author(name="{}#{}".format(message.author.name,
                                                    message.author.discriminator),
                                icon_url=str(
                                    message.author.avatar_url_as(
                                        static_format="png", size=1024)))
                if message.content != "":
                    embed.add_field(name="Content", value=message.content)
                if len(message.attachments) != 0:
                    embed.add_field(name="Attachments",
                                    value=", \n".join(
                                        a.url for a in message.attachments))
                embed.set_footer(text="Author ID: {} | Message ID: {}".format(
                    message.author.id, message.id))
                await channel.send(embed=embed)




def setup(bot):
    bot.add_cog(AuditLog(bot))