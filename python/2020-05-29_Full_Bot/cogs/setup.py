# DND

import discord
from discord.ext import commands
import os

import cogs.mongohelper as mongo
import cogs.functions as functions


def botembed():
    return functions.embed("Bot Setup", color=0x838383)


class Setup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def cogs(self, ctx):
        directory = os.path.dirname(os.path.realpath(__file__))
        disabled = mongo.find(mongo.SETTINGS, "cogs")["disabled"]
        enabled = mongo.find(mongo.SETTINGS, "cogs")["enabled"]

        if len(enabled) < 1:
            ecogs = "None"
        else:
            ecogs = ""

        if len(disabled) < 1:
            dcogs = "None"
        else:
            dcogs = ""

        for cog in enabled:
            with open(os.path.join(directory, cog + ".py")) as f:
                content = f.read()
            if "# DND" in content:  # "DND": Do Not Deactivate - prevents cogs from being deactivated
                ecogs += "- **`{}`**\n".format(cog)
            else:
                ecogs += "- `{}`\n".format(cog)

        for cog in disabled:
            with open(os.path.join(directory, cog + ".py")) as f:
                content = f.read()
            if "# DND" in content:  # "DND": Do Not Deactivate - prevents cogs from being deactivated
                dcogs += "- **`{}`**\n".format(cog)
            else:
                dcogs += "- `{}`\n".format(cog)

        embed = botembed()
        embed.description = "Cogs are individual pieces of the bot's code that do different tasks.\nThe state of cogs in bold text (**like this**) cannot be changed - those cogs cannot be deactivated."
        embed.add_field(name="Enabled Cogs", value=ecogs)
        embed.add_field(name="Disabled Cogs", value=dcogs)
        await ctx.send(embed=embed)

    @commands.command()
    async def enable(self, ctx, cog=None):
        if not functions.isowner(ctx.message.author):
            embed = functions.error(
                "You do not have permission to use this command! Only the bot owner can use this command."
            )
        if cog is None:
            embed = functions.error(
                "Please specify a disabled cog to enable (use the `cogs` command to see the list of cogs)."
            )
            return await ctx.send(embed=embed)
        cog = cog.lower().strip()
        disabled = mongo.find(mongo.SETTINGS, "cogs")["disabled"]
        enabled = mongo.find(mongo.SETTINGS, "cogs")["enabled"]
        if cog not in enabled and cog not in disabled:
            embed = functions.error(
                "Could not find cog with name `{}`.".format(cog))
            return await ctx.send(embed=embed)
        if cog not in disabled:
            embed = functions.error(
                "The `{}` cog is already enabled.".format(cog))
            return await ctx.send(embed=embed)
        mongo.update(mongo.SETTINGS, "cogs", {"enabled": enabled.append(cog)})
        mongo.update(mongo.SETTINGS, "cogs",
                     {"disabled": disabled.remove(cog)})
        self.bot.load_extension(cog)
        embed = botembed()
        embed.description = "Successfully changed the state of the `{}` cog to `enabled`.".format(
            cog)
        return await ctx.send(embed=embed)

    @commands.command()
    async def disable(self, ctx, cog=None):
        if not functions.isowner(ctx.message.author):
            embed = functions.error(
                "You do not have permission to use this command! Only the bot owner can use this command."
            )
        if cog is None:
            embed = functions.error(
                "Please specify a disabled cog to enable (use the `cogs` command to see the list of cogs)."
            )
            return await ctx.send(embed=embed)
        cog = cog.lower().strip()
        disabled = mongo.find(mongo.SETTINGS, "cogs")["disabled"]
        enabled = mongo.find(mongo.SETTINGS, "cogs")["enabled"]
        if cog not in enabled and cog not in disabled:
            embed = functions.error(
                "Could not find cog with name `{}`.".format(cog))
            return await ctx.send(embed=embed)
        if cog not in enabled:
            embed = functions.error(
                "The `{}` cog is already enabled.".format(cog))
            return await ctx.send(embed=embed)
        directory = os.path.dirname(os.path.realpath(__file__))
        with open(os.path.join(directory, cog + ".py")) as f:
            content = f.read()
        if "# DND" in content:
            embed = functions.error(
                "The `{}` cog cannot be disabled.".format(cog))
        mongo.update(mongo.SETTINGS, "cogs",
                     {"disabled": disabled.append(cog)})
        mongo.update(mongo.SETTINGS, "cogs", {"enabled": enabled.remove(cog)})
        self.bot.load_extension(cog)
        embed = botembed()
        embed.description = "Successfully changed the state of the `{}` cog to `enabled`.".format(
            cog)
        return await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Setup(bot))
