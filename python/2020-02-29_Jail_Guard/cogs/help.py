import discord
from discord.ext import commands
#import resource

import cogs.functions as functions
import cogs.settings as settings

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def addhelp(self, embed, command, description):
        embed.add_field(name="{}{}".format(settings.prefix, command),
                        value=description,
                        inline=False)
        return embed


    @commands.command()
    async def status(self, ctx):
        message = ""
        if ctx.guild.id == "[REDACTED]":
            bots = [m for m in ctx.guild.members if m.bot]
            for b in bots:
                message += "<@{}>: **{}**\n".format(b.id, str(b.status).title())
        embed = functions.botembed("Status", message, settings.BLUE)

        pingtime = round(self.bot.latency * 1000, 3)
        kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        memoryusage = str(round(kb / 1024, 2))

        embed.add_field(name="Ping", value="{} ms".format(pingtime))
        embed.add_field(name="Memory Usage", value="{} MB".format(memoryusage))
        embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon_url))
        await ctx.send(embed=embed)

    @commands.command()
    async def help(self, ctx):
        embed = functions.botembed("Help", "", settings.BLUE)
        embed.set_author(name=ctx.guild.name, icon_url=str(ctx.guild.icon_url))
        embed.add_field(name="Prefix",
                        value="The prefix for this bot is `{}`".format(
                            settings.PREFIX),
                        inline=False)
        embed = addhelp(embed, "help", "Shows this message")
        if ctx.guild.id == "[REDACTED]":
            embed = addhelp(
                embed, "status",
                "Shows the status of all bots, along with additional info for this bot."
            )
            embed = addhelp(
                embed, "ban <user> [reason] [reporter ***ID***]",
                "Bans a user from the server, and invites them to the ban appeal server."
            )
            embed = addhelp(
                embed, "blacklist <user> [reason] [reporter ***ID***]",
                "Bans a user from the server. Unlike the normal `ban` command, the banned user is not invited into the ban appeal server."
            )
        elif ctx.guild.id == "[REDACTED]":
            embed = addhelp(embed, "status", "Shows info for this bot.")

            embed = addhelp(embed, "appeal <appeal>", "Sends a ban appeal.")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Help(bot))