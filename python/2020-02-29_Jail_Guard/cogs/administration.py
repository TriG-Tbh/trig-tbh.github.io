import discord
from discord.ext import commands
import datetime

import cogs.functions as functions
import cogs.settings as settings

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def warn(self, ctx, member: discord.Member = None, duration=None, *reason):
        if ctx.guild.id != "[REDACTED]":
            return
        reporter = None
        if not ctx.channel.permissions_for(ctx.message.author).ban_members:
            embed = functions.botembed("Error",
                            "You do not have permission to use this command.",
                            settings.RED)
            return await ctx.send(embed=embed)
        blacklist = ["[REDACTED]"]
        if member.id in blacklist:
            embed = functions.botembed("Error", "Please specify a member to warn.", settings.RED)
            return await ctx.send(embed=embed)

        if "[REDACTED]" in [r.id for r in member.roles]:
            embed = functions.botembed(
                "Notice",
                "<@{}> is already on warn 2. If you want to ban them, use `{}ban` or `{}blacklist`."
                .format(member.id, settings.prefix, settings.prefix), settings.BLUE)
            return await ctx.send(embed=embed)

        if len(reason) > 0:
            reporter = reason[-1]
            reasontemp = list(reason).copy()[:-1]
            reporter = reporter.replace("<@", "").replace(">", "")
            try:
                reporter = int(reporter)
            except:
                reason = " ".join(reason)
                reporter = None
            else:
                reporter = int(reporter)
                reason = " ".join(reasontemp)
        else:
            reason = "No reason specified"
        now = datetime.datetime.now()

        duration = [c for c in duration]

        intervals = []

        alphabet = "abcdefghijklmnopqrstuvwxyz"
        stop = 0
        for i in range(len(duration)):
            if duration[i] in alphabet:
                interval = duration[stop:i + 1]
                interval = "".join(interval)
                intervals.append(interval)
                print(interval)
                stop = i + 1

        for i in intervals:
            num = int(i[:-1])
            if i.endswith('s'):
                now += datetime.timedelta(seconds=num)
            elif i.endswith('m'):
                now += datetime.timedelta(minutes=num)
            elif i.endswith('h'):
                now += datetime.timedelta(hours=num)
            elif i.endswith('d'):
                now += datetime.timedelta(days=num)
            else:
                continue

        if not await functions.confirmation(self.bot, ctx):
            return

        warn = 1
        if 596201848399069196 in [r.id for r in member.roles]:
            warn = 2

        expiration = now.strftime("%B %d")

        message = ":no_entry_sign: Warn {} - <@{}>\n:pencil: Reason - {}\n:calendar: Expires - {}{}".format(
            warn, member.id, reason, expiration,
            ("\n:sparkles: Reporter: <@{}>".format(reporter)
            if reporter is not None else ""))
        channel = bot.get_channel("[REDACTED]")
        await channel.send(message)
        role = None

        if warn == 1:
            role = discord.utils.find(lambda r: r.id == "[REDACTED]",
                                    ctx.guild.roles)
        elif warn == 2:
            role = discord.utils.find(lambda r: r.id == "[REDACTED]",
                                    ctx.guild.roles)
        await member.add_roles(role)


    @commands.command()
    async def blacklist(self, ctx, member: discord.Member = None, *reason):
        if ctx.guild.id != "[REDACTED]":
            return
        reporter = None
        if not ctx.channel.permissions_for(ctx.message.author).ban_members:
            embed = functions.botembed("Error",
                            "You do not have permission to use this command.",
                            settings.RED)
            return await ctx.send(embed=embed)
        blacklist = ["[REDACTED]"]
        if member.id in blacklist:
            embed = functions.botembed("Error", "Please specify a member to ban.", settings.RED)
            return await ctx.send(embed=embed)
        if len(reason) > 0:
            reporter = reason[-1]
            reasontemp = list(reason).copy()[:-1]
            reporter = reporter.replace("<@", "").replace(">", "")
            try:
                reporter = int(reporter)
            except:
                reason = " ".join(reason)
                reporter = None
            else:
                reporter = int(reporter)
                reason = " ".join(reasontemp)
        else:
            reason = "No reason specified"
        message = """You have been banned from the [REDACTED] server for the following reason:
    **`{}`**
    Due to the nature of your ban, you will not be given the opportunity to appeal your ban.""".format(
            reason)
        if not await functions.confirmation(self.bot, ctx):
            return
        embed = functions.botembed("Ban", message, settings.RED)
        await member.send(message)
        channel = bot.get_channel("[REDACTED]")
        try:
            await member.guild.ban(member, reason=reason, delete_message_days=0)
        except Exception as e:
            embed = functions.botembed(
                "Error",
                "Could not ban <@{}> due to the following error: `{}`".format(
                    member.id, str(e)), settings.RED)
            await ctx.send(embed=embed)
        else:
            await channel.send(
                "<:ban:[REDACTED]> Ban (Blacklist) - <@{}>\n:pencil: Reason - {}{}"
                .format(member.id, reason,
                        ("\n:sparkles: Reporter: <@{}>".format(reporter)
                        if reporter is not None else "")))

    

    @commands.command(aliases=["ban"])
    async def dothebanthing(self, ctx, member: discord.Member = None, *reason):
        if ctx.guild.id != "[REDACTED]":
            return
        reporter = None
        if not ctx.channel.permissions_for(ctx.message.author).ban_members:
            embed = functions.botembed("Error",
                            "You do not have permission to use this command.",
                            settings.RED)
            return await ctx.send(embed=embed)
        blacklist = ["[REDACTED]"]
        if member.id in blacklist:
            embed = functions.botembed("Error", "Please specify a member to ban.", settings.RED)
            return await ctx.send(embed=embed)
        if len(reason) > 0:
            reporter = reason[-1]
            reasontemp = list(reason).copy()[:-1]
            reporter = reporter.replace("<@", "").replace(">", "")
            try:
                reporter = int(reporter)
            except:
                reason = " ".join(reason)
                reporter = None
            else:
                reporter = int(reporter)
                reason = " ".join(reasontemp)
        else:
            reason = "No reason specified"
        message = """You have been banned from the [REDACTED] server for the following reason:
    **`{}`**
    If you want to appeal your ban, join [REDACTED] and use `{}appeal [reason why you should be unbanned]`.
    Your appeal will be looked at by the admins of the server. If the majority of them vote in favor of your appeal, you will be unbanned.
    """.format(reason, settings.prefix)
        if not await functions.confirmation(ctx):
            return
        embed = functions.botembed("Ban", message, settings.RED)
        await member.send(message)
        channel = bot.get_channel("[REDACTED]")
        try:
            await member.guild.ban(member, reason=reason, delete_message_days=0)
        except Exception as e:
            embed = functions.botembed(
                "Error",
                "Could not ban <@{}> due to the following error: `{}`".format(
                    member.id, str(e)), settings.RED)
            await ctx.send(embed=embed)
        else:
            await channel.send(
                "<:ban:[REDACTED]> Ban - <@{}>\n:pencil: Reason - {}{}".
                format(member.id, reason,
                    ("\n:sparkles: Reporter: <@{}>".format(reporter)
                        if reporter is not None else "")))



def setup(bot):
    bot.add_cog(Admin(bot))