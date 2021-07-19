import discord
from discord.ext import commands

import cogs.functions as functions
import cogs.settings as settings


class AppealsManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def get_appeal_text(self, appeal):
        try:
            return appeal.embed.description
        except:
            return None

    async def get_appeal(self, member):
        channel = self.bot.get_channel("[REDACTED]")
        appeals = [a for a in await channel.history(limit=None).flatten()]
        print(appeals)
        for a in appeals:
            try:
                _ = a.embed.author
            except Exception as e:
                print(str(e))
                if "<@{}>".format(member.id) in a.content:
                    return a
            else:
                if member.name + "#" + str(
                        member.discriminator) in a.embed.author:
                    return a
        return None

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)

        if message.guild.id != "[REDACTED]":
            return

        reactions = message.reactions
        yes = reactions[0].count - 1

        no = reactions[1].count - 1

        roleid = "[REDACTED]"
        voters = len([
            m for m in message.guild.members
            if roleid in [r.id for r in m.roles]
        ])

        if len(message.mentions) > 0:
            target = message.mentions[0]
        else:
            title = message.embeds[0].author.name
            targetstr = title.replace("New appeal from ", "")
            if "<@" in targetstr and ">" in targetstr:
                target = int(
                    targetstr.replace("<@", "").replace("<@!",
                                                        "").replace(">", ""))
                target = discord.utils.find(lambda m: m.id == target,
                                            message.guild.members)
                if target is None:
                    await message.delete()
                    embed = functions.botembed(
                        "Appeal Not Found",
                        "The appeal sent by `{}` could not be found. If this is your old name, please resubmit your appeal.\nIf the appeal has been manually accepted or rejected, no further action is required."
                        .format(targetstr), settings.YELLOW)
                    channel = self.bot.get_channel("[REDACTED]")
                    await channel.send(embed=embed)
            elif "#" in targetstr:
                name = targetstr.split("#")[:-1]
                name = "#".join(name)
                target = discord.utils.find(lambda m: m.name == name,
                                            message.guild.members)
                if target is None:
                    await message.delete()
                    embed = functions.botembed(
                        "Appeal Not Found",
                        "The appeal sent by `{}` could not be found. If this is your old name, please resubmit your appeal.\nIf the appeal has been manually accepted or rejected, no further action is required."
                        .format(targetstr), settings.YELLOW)
                    channel = self.bot.get_channel("[REDACTED]")
                    await channel.send(embed=embed)

        if yes / voters > 0.5:
            userid = target.id
            user = await self.bot.fetch_user(userid)
            guild = self.bot.get_guild("[REDACTED]")
            await guild.unban(user, reason="Appeal accepted")
            embed = functions.botembed(
                "Appeal Accepted",
                "Your appeal has been accepted. Make sure to read and follow the rules so you don't get banned, as you don't get a second chance.\nInvite link: [REDACTED]",
                settings.GREEN)
            await user.send(embed=embed)
            guild = self.bot.get_guild("[REDACTED]")
            await guild.ban(user, reason="Ban apppeal has been accepted.")
            await message.delete()
            channel = self.bot.get_channel("[REDACTED]")
            embed = functions.botembed(
                "Appeal Accepted",
                "The appeal sent by <@{}> has been accepted".format(userid),
                settings.GREEN)
            await channel.send(embed=embed)
            channel = self.bot.get_channel("[REDACTED]")
            await channel.send(
                ":white_check_mark: Unban - @{}#{}\n:pencil: Reason - enforcer vote (appeal accepted)"
                .format(user.name, user.discriminator))
        elif no / voters > 0.5:
            userid = target.id
            user = await self.bot.fetch_user(userid)
            embed = functions.botembed(
                "Appeal Declined",
                "Your appeal has been rejected. If permitted by staff, you can revise your appeal and resubmit it.",
                settings.RED)
            await user.send(embed=embed)

            await message.delete()
            channel = self.bot.get_channel("[REDACTED]")
            embed = functions.botembed(
                "Appeal Declined",
                "The appeal sent by <@{}> has been declined".format(userid),
                settings.RED)
            await channel.send(embed=embed)

    @commands.command(aliases=["submit"])
    async def appeal(self, ctx, *, appeal):
        if ctx.guild.id != "[REDACTED]":
            return
        role = discord.utils.find(lambda r: r.id == "[REDACTED]",
                                  ctx.message.author.guild.roles)
        if ctx.message.author.top_role != role:
            embed = functions.botembed(
                "Error", "You are not a prisoner! You can't send an appeal.",
                settings.RED)
            return await ctx.send(embed=embed)
        if await self.get_appeal(ctx.message.author) is not None:
            embed = functions.botembed(
                "Error",
                "You already have an appeal sumbitted! Use `{}edit` to edit your appeal."
                .format(settings.prefix), settings.RED)
            return await ctx.send(embed=embed)
        if len(appeal) == 0:
            embed = functions.botembed(
                "Error",
                "Your appeal cannot be empty! Plesae resubmit your appeal.",
                settings.RED)
            return await ctx.send(embed=embed)
        embed = functions.botembed("", appeal, settings.BLUE)
        embed.set_author(name="New appeal from {}#{}".format(
            ctx.message.author.name, ctx.message.author.discriminator),
                         icon_url=str(
                             ctx.message.author.avatar_url_as(
                                 static_format="png", size=1024)))
        channel = self.bot.get_channel("[REDACTED]")
        log = await channel.send(
            "<@&[REDACTED]> A new appeal has been submitted by <@{}>".
            format(ctx.message.author.id),
            embed=embed)
        await log.add_reaction("✅")
        await log.add_reaction("❌")
        embed = functions.botembed(
            "Appeal submitted",
            "Your appeal has been submitted. The moderators will vote on your appeal.",
            settings.GREEN)
        await ctx.send(embed=embed)

    @commands.command()
    async def edit(self, ctx, *, appeal):
        if ctx.guild.id != "[REDACTED]":
            return
        if await self.get_appeal(ctx.message.author) is None:
            embed = functions.botembed(
                "Error",
                "You haven't submitted an appeal! Use `{}appeal` to submit one."
                .format(settings.prefix), settings.RED)
            return await ctx.send(embed=embed)
        if len(appeal) == 0:
            embed = functions.botembed(
                "Error",
                "Your appeal cannot be empty! Plesae resubmit your appeal.",
                settings.RED)
            return await ctx.send(embed=embed)

        embed = functions.botembed("", appeal, settings.BLUE)
        embed.set_author(name="New appeal from {}#{}".format(
            ctx.message.author.name, ctx.message.author.discriminator),
                         icon_url=str(
                             ctx.message.author.avatar_url_as(
                                 static_format="png", size=1024)))

        oldappeal = await self.get_appeal(ctx.message.author)
        await oldappeal.edit(
            content=
            "<@&[REDACTED]> A new appeal has been submitted by <@{}>".
            format(ctx.message.author.id),
            embed=embed)

        embed = functions.botembed("Appeal edited",
                                   "Your appeal has been edited.",
                                   settings.GREEN)
        await ctx.send(embed=embed)

    @commands.command()
    async def remote(self, ctx, user: discord.Member, *, appeal):
        if "[REDACTED]" not in [
                role.id for role in ctx.message.author.roles
        ]:
            embed = functions.botembed(
                "Error", "You are not a guard! You cannot use this command.",
                settings.RED)
            return await ctx.send(embed=embed)
        if len(appeal) == 0:
            embed = functions.botembed(
                "Error",
                "Your appeal cannot be empty! Plesae resubmit your appeal.",
                settings.RED)
            return await ctx.send(embed=embed)
        embed = functions.botembed("", appeal, settings.BLUE)

        embed.set_author(
            name="New appeal from {}#{}".format(user.name, user.discriminator),
            icon_url=str(user.avatar_url_as(static_format="png", size=1024)))
        channel = self.bot.get_channel("[REDACTED]")
        log = await channel.send(
            "<@&[REDACTED]> A new appeal has been submitted by <@{}>".
            format(user.id),
            embed=embed)
        await log.add_reaction("✅")
        await log.add_reaction("❌")
        embed = functions.botembed(
            "Appeal submitted",
            "The appeal for <@{}> has been remotely submitted.".format(
                user.id), settings.GREEN)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AppealsManager(bot))