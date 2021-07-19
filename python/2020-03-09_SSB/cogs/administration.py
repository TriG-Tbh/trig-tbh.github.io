from discord.ext import commands
import functions
import random
import discord
import asyncio

def botembed():
    embed = functions.embed("Administration", color=0x8b0000)
    return embed

def auditlogembed():
    embed = functions.embed("Audit Log", color=0x72bcd4)
    return embed

class Administration(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirmation(self, ctx):
        values = [c for c in "0123456789"]
        code = ""
        for _ in range(4):
            code += random.choice(values)
        def check(message):
            return message.content == code and message.channel == ctx.message.channel and message.author == ctx.message.author
        embed = botembed()
        embed.add_field(name="Confirmation", value="Are you sure you want to proceed? Type `{}` to proceed, or `cancel` to cancel.".format(code), inline=False)
        message = await ctx.send(embed=embed)
        try:
            _ = await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            embed = botembed()
            embed.add_field(name="Confirmation", value="Confirmation failed. Please run command again.")
            await message.edit(embed=embed)
            return False
        else:
            if message.content.lower().strip().lstrip() == "cancel":
                embed = botembed()
                embed.add_field(name="Confirmation", value="Confirmation failed. Please run command again.")
                await message.edit(embed=embed)
                return False
            await message.delete()
            return True

    @commands.command()
    async def whois(self, ctx, user=None):
        if user is None:
            user = ctx.message.author
        else:
            if user is not None:
                if len(ctx.message.mentions) > 0:
                    if ctx.message.mentions[0] not in ctx.guild.members:
                        embed = botembed()
                        embed.add_field(name="Error", value="Invalid parameter - please specify a user in the server to look up.", inline=False)
                        return await ctx.send(embed=embed)
                    user = ctx.message.mentions[0]
                else:
                    try:
                        user = int(user)
                    except:
                        embed = botembed()
                        embed.add_field(name="Error", value="Invalid parameter - invalid user ID.", inline=False)
                        return await ctx.send(embed=embed)
                    user = discord.utils.find(lambda m: m.id == user, ctx.guild.members)
                    if user is None:
                        embed = botembed()
                        embed.add_field(name="Error", value="Invalid parameter - please specify a user in the server to look up.", inline=False)
                        return await ctx.send(embed=embed)
        name = user.name
        discriminator = user.discriminator
        userid = user.id
        joined_at = user.joined_at.strftime("%a, %b. %d, %Y at %I:%M:%S %p")
        sortedlist = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        joinpos = sortedlist.index(user)
        registered_at = user.created_at.strftime("%a, %b. %d, %Y at %I:%M:%S %p")
        roletext = ""
        for role in user.roles:
            if role.name != "@everyone":
                roletext += "<@&{}> ".format(role.id)
        roletext = roletext.strip()
        embed = botembed()
        embed.set_thumbnail(url=str(user.avatar_url_as(static_format="png")))
        embed.add_field(name="User", value="{}#{}".format(name, discriminator), inline=False)
        embed.add_field(name="Tag", value="<@{}>".format(userid), inline=False)
        embed.add_field(name="Registered", value=registered_at, inline=False)
        embed.add_field(name="Joined", value=joined_at, inline=False)
        embed.add_field(name="Join Position", value=joinpos, inline=False)
        if roletext != "":
            embed.add_field(name="Roles", value=roletext, inline=False)
        return await ctx.send(embed=embed)

    @commands.command()
    async def proxy(self, ctx, user=None, *message):
        if user is not None and len(ctx.message.mentions) == 0:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to sent a message to.", inline=False)
            return await ctx.send(embed=embed)
        if user is None and len(message) == 0:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to sent a message to, as well as a message to send.", inline=False)
            return await ctx.send(embed=embed)
        if user is not None and len(message) == 0:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a message to send.", inline=False)
            return await ctx.send(embed=embed)
        message = " ".join(message)
        target = ctx.message.mentions[0]
        embed = botembed()
        embed.add_field(name="Message sent by {}#{}".format(ctx.message.author.name, ctx.message.author.discriminator), value=message, inline=False)
        try:
            await target.send(embed=embed)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Unable to send message to <@{}>.".format(target.id), inline=False)
            return await ctx.send(embed=embed)
        else:
            embed = botembed()
            embed.add_field(name="Message sent", value="Successfully sent message to <@{}>: `{}`.".format(target.id, message), inline=False)
            return await ctx.send(embed=embed)

    @commands.command()
    async def hackban(self, ctx, user=None, *reason):
        if user is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to hackban.", inline=False)
            return await ctx.send(embed=embed)
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0].id
        else:
            try:
                user = int(user)
            except:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - please specify a user to hackban.", inline=False)
                return await ctx.send(embed=embed)        
        isinserver = discord.utils.find(lambda m: m.id == user, ctx.guild.members)
        if isinserver is not None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> is in the server. If you want to ban them, use `ban`.".format(user), inline=False)
            return await ctx.send(embed=embed)
        if user == self.bot.user.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - I cannot ban myself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.author.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot ban yourself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.guild.owner.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot ban the owner!", inline=False)
            return await ctx.send(embed=embed)
        try:
            usertoban = await self.bot.fetch_user(user)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user does not exist. Please specify a user to hackban.", inline=False)
            return await ctx.send(embed=embed)
        if usertoban in [ban.user for ban in await ctx.guild.bans()]:
            ban = await ctx.guild.fetch_ban(usertoban)
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> has already been banned for `{}`".format(usertoban.id, ban.reason), inline=False)
            return await ctx.send(embed=embed)
        confirm = await self.confirmation(ctx)
        if len(reason) > 0:
            reason = "hackban - " + " ".join(reason)
        else:
            reason = "hackban - no reason given"
        if confirm:
            await ctx.guild.ban(usertoban, reason=reason)
            embed = botembed()
            embed.add_field(name="Success", value="Successfully hackbanned <@{}>".format(user), inline=False)
            await ctx.send(embed=embed)


    @commands.command()
    async def ban(self, ctx, user=None, *reason):
        if user is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to ban.", inline=False)
            return await ctx.send(embed=embed)
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0].id
        else:
            try:
                user = int(user)
            except:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - please specify a user to ban.", inline=False)
                return await ctx.send(embed=embed)        
        isinserver = discord.utils.find(lambda m: m.id == user, ctx.guild.members)
        if isinserver is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> is not in the server. If you want to ban them, use `hackban`.".format(user), inline=False)
            return await ctx.send(embed=embed)
        if user == self.bot.user.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - I cannot ban myself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.author.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot ban yourself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.guild.owner.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot ban the owner!", inline=False)
            return await ctx.send(embed=embed)
        try:
            usertoban = await self.bot.fetch_user(user)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user does not exist. Please specify a user to ban.", inline=False)
            return await ctx.send(embed=embed)
        if usertoban in [ban.user for ban in await ctx.guild.bans()]:
            ban = await ctx.guild.fetch_ban(usertoban)
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> has already been banned for `{}`".format(usertoban.id, ban.reason), inline=False)
            return await ctx.send(embed=embed)
        confirm = await self.confirmation(ctx)
        if len(reason) > 0:
            reason = " ".join(reason)
        else:
            reason = "no reason given"
        if confirm:
            await ctx.guild.ban(usertoban, reason=reason)
            embed = botembed()
            embed.add_field(name="Success", value="Successfully banned <@{}>".format(user), inline=False)
            await ctx.send(embed=embed)


    @commands.command()
    async def unban(self, ctx, user=None, *reason):
        if user is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to ban.", inline=False)
            return await ctx.send(embed=embed)
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0].id
        else:
            try:
                user = int(user)
            except:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - please specify a user to ban.", inline=False)
                return await ctx.send(embed=embed)        
        isinserver = discord.utils.find(lambda m: m.id == user, ctx.guild.members)
        if isinserver is not None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> is in the server.".format(user), inline=False)
            return await ctx.send(embed=embed)
        if user == self.bot.user.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - I cannot unban myself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.author.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot unban yourself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.guild.owner.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot unban the owner!", inline=False)
            return await ctx.send(embed=embed)
        try:
            usertoban = await self.bot.fetch_user(user)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user does not exist. Please specify a user to unban.", inline=False)
            return await ctx.send(embed=embed)
        if usertoban not in [ban.user for ban in await ctx.guild.bans()]:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> is not banned.", inline=False)
            return await ctx.send(embed=embed)
        confirm = await self.confirmation(ctx)
        if len(reason) > 0:
            reason = " ".join(reason)
        else:
            reason = "no reason given"
        if confirm:
            await ctx.guild.unban(usertoban, reason=reason)
            embed = botembed()
            embed.add_field(name="Success", value="Successfully unbanned <@{}>".format(user), inline=False)
            await ctx.send(embed=embed)
            embed = auditlogembed()
            embed.set_thumbnail(url=str(usertoban.avatar_url_as(static_format="png", size=1024)))
            embed.add_field(name="Member Unbanned", value="<@{}> {}#{}".format(usertoban.id, usertoban.name, usertoban.discriminator), inline=False)
            channel = self.bot.get_channel("[REDACTED]")
            return await channel.send(embed=embed)

    @commands.command()
    async def kick(self, ctx, user=None, *reason):
        if user is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a user to kick.", inline=False)
            return await ctx.send(embed=embed)
        if len(ctx.message.mentions) > 0:
            user = ctx.message.mentions[0].id
        else:
            try:
                user = int(user)
            except:
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - please specify a user to kick.", inline=False)
                return await ctx.send(embed=embed)        
        isinserver = discord.utils.find(lambda m: m.id == user, ctx.guild.members)
        if isinserver is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user <@{}> is not in the server.".format(user), inline=False)
            return await ctx.send(embed=embed)
        if user == self.bot.user.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - I cannot kick myself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.author.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot kick yourself!", inline=False)
            return await ctx.send(embed=embed)
        elif user == ctx.guild.owner.id:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - you cannot kick the owner!", inline=False)
            return await ctx.send(embed=embed)
        try:
            usertoban = await self.bot.fetch_user(user)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - user does not exist. Please specify a user to kick.", inline=False)
            return await ctx.send(embed=embed)
        confirm = await self.confirmation(ctx)
        if len(reason) > 0:
            reason = " ".join(reason)
        else:
            reason = "no reason given"
        if confirm:
            await ctx.guild.kick(usertoban, reason=reason)
            embed = botembed()
            embed.add_field(name="Success", value="Successfully kicked <@{}>".format(user), inline=False)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Administration(bot))