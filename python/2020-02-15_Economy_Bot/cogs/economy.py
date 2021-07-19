import discord
from discord.ext import commands

import random
import json
import os
import asyncio

def join(name):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), name)

def botembed(title):
    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.set_author(name=title)
    return embed

def helpembed(prefix):
    embed = botembed("Help (Economy)")
    embed.add_field(name="{}balance/bal/b [user mention]".format(prefix), value="Gets your balance, or the balance of a specified user")
    embed.add_field(name="{}leaderboard/top".format(prefix), value="Displays the top 5 users in the server")
    embed.add_field(name="{}beg".format(prefix), value="Recieve a small amount of coins. You have a low chance of recieving coins.")
    embed.add_field(name="{}steal <user mention>".format(prefix), value="Steal up to half of a user's coins. Will only work if they are offline. Can only be usde once every 24 hours.")
    embed.add_field(name="{}pay <user mention> <amount>".format(prefix), value="Pays a specified user a specified amount of coins.")
    embed.add_field(name="{}daily".format(prefix), value="Recieve a daily amount of coins. Can only be used once every 24 hours.")
    return embed

def read_coins(id):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            return None
        else:
            return values[id]
        
def add_coins(id, amount):
    id = str(id)
    with open(join("economy.json")) as f:
        values = json.load(f)
        if id not in values.keys():
            values[id] = 0
        values[id] += amount
        with open(join("economy.json"), "w") as nf:
            json.dump(values, nf)



class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def confirmation(self, ctx):
        values = [c for c in "0123456789"]
        code = ""
        for _ in range(4):
            code += random.choice(values)
        def check(message):
            return message.content == code and message.channel == ctx.message.channel and message.author == ctx.message.author
        embed = botembed("Economy")
        embed.add_field(name="Confirmation", value="Are you sure you want to proceed? Type `{}` to proceed.".format(code))
        message = await ctx.send(embed=embed)
        try:
            _ = await self.bot.wait_for("message", check=check, timeout=60.0)
        except asyncio.TimeoutError:
            return False, message
        else:
            return True, message

    def getboard(self, member):
        board = {}
        for m in member.guild.members:
            value = read_coins(m.id)
            if value is None or value == 0:
                continue
            else:
                board[m.id] = value
        sorteddict = sorted(board.items(), key=lambda x: x[1], reverse=True)
        return sorteddict

    @commands.command(aliases=['top'])
    async def leaderboard(self, ctx):
        board = self.getboard(ctx.message.author)
        embed = botembed("Economy")
        top = []
        if len(board) >= 5:
            top = board[:5]
        elif len(board) == 0:
            embed.add_field(name="Leaderboard empty", value="There is nobody on the leaderboard. Talk to get started!")
            return await ctx.send(embed=embed)
        else:
            top = board
        for i in range(len(top)):
            embed.add_field(name="Position #{}".format(i + 1), value="<@{}>, with **{} coin{}**".format(top[i][0], top[i][1], ("s" if top[i][1] != 1 else "")))
        await ctx.send(embed=embed)


    @commands.command(aliases=["b", "bal"])
    async def balance(self, ctx, user=None):
        if user is None:
            authorid = str(ctx.message.author.id)
        else:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to see the amount of coins they have.")
                return await ctx.send(embed=embed)
            else:
                mentioned = ctx.message.mentions[0]
                if mentioned.bot:
                    embed = botembed("Economy")
                    embed.add_field(name="Error", value="That user is a bot! Bots do not obtain coins.")
                    return await ctx.send(embed=embed)
                authorid = str(mentioned.id)
        with open(join("economy.json")) as f:
            values = json.load(f)
        try:
            value = values[authorid]
        except KeyError:
            embed = botembed("Economy")
            if authorid == ctx.message.author.id:
                embed.add_field(name="Error", value="You have no coins. Start talking to get coins!")
            else:
                embed.add_field(name="Error", value="That user has no coins.")
            return await ctx.send(embed=embed)
        member = discord.utils.find(lambda m: m.id == int(authorid), ctx.guild.members)
        embed = botembed("Economy")
        aoran = ""
        if value == 1:
            aoran = ""
        else:
            aoran = "s"
        embed.add_field(name="Balance for {}".format(member.name), value="Balance: **{} coin{}**".format(value, aoran))
        board = self.getboard(member)
        place = [p for p in board if p[0] == member.id]
        if len(place) == 0:
            embed = botembed("Economy")
            if member.id == ctx.message.author.id:
                embed.add_field(name="Error", value="You have no coins. Start talking to get coins!")
            else:
                embed.add_field(name="Error", value="That user has no coins.")
            return await ctx.send(embed=embed)
        else:
            position = board.index(place[0]) + 1

        embed.add_field(name="Leaderboard", value="You are currently #{} in the leaderboard.".format(position))
        return await ctx.send(embed=embed)

    @commands.command()
    async def beg(self, ctx):
        success = random.randint(1, 20)
        if success == 20:
            coins = random.randint(1, 5)
            add_coins(ctx.message.author.id, coins)
            aoran = "" if coins == 1 else "s"
            embed = botembed("Economy")
            embed.add_field(name="Success!", value="Your begging paid off! You recieved **{} coin{}**.".format(coins, aoran))
            return await ctx.send(embed=embed)
        else:
            embed = botembed("Economy")
            embed.add_field(name="Failure", value="Though you tried your best, your begging did not pay off. You recieved **0 coins**.")
            return await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def steal(self, ctx):
        if len(ctx.message.mentions) == 0:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - mention a user to steal a random amount of coins.")
            return await ctx.send(embed=embed)
        member = ctx.message.mentions[0]
        if member.id == ctx.message.author.id:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - you can't steal from yourself!")
            return await ctx.send(embed=embed)
        target = read_coins(member.id)
        if target is None:
            embed = botembed("Economy")
            embed.add_field(name="Failure", value="That user does not have any coins!")
            return await ctx.send(embed=embed)
        elif target == 0:
            embed = botembed("Economy")
            embed.add_field(name="Failure", value="That user does not have any coins!")
            return await ctx.send(embed=embed)
        if member.status == discord.Status.offline:
            amount = random.randint(1, target // 2)
            add_coins(member.id, -amount)
            add_coins(ctx.message.author.id, amount)
            aoran = "" if amount == 1 else "s"
            embed = botembed("Economy")
            embed.add_field(name="Success", value="Congratulations, you're a criminal! You successfully stole {} coin{}.".format(amount, aoran))
            return await ctx.send(embed=embed)
        else:
            embed = botembed("Economy")
            embed.add_field(name="Failure", value="That user is online! They noticed you trying to steal their coins. Though you barely escaped with your life, you didn't steal any coins...")
            return await ctx.send(embed=embed)

    @commands.command()
    async def give(self, ctx, user=None, amount=None):
        if ctx.message.author.id != 424991711564136448:
            return
        if user is None:
            id = ctx.message.author.id
        else:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to give coins to.")
                return await ctx.send(embed=embed)
            else:
                if ctx.message.mentions[0].bot:
                    embed = botembed("Economy")
                    embed.add_field(name="Error", value="Invalid parameter - you can't give coins to a bot!")
                    return await ctx.send(embed=embed)
                id = ctx.message.mentions[0].id
        

        if amount is None:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins not specified.")
            return await ctx.send(embed=embed)
        

        try:
            amount = int(amount)
        except:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        else:
            if amount == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - you can't give 0 coins to someone!")
                return await ctx.send(embed=embed)
            valid, message = await self.confirmation(ctx)
            if valid:
                await message.delete()
                add_coins(id, amount)
                embed = botembed("Economy")
                if amount > 1:
                    embed.add_field(name="Success", value="Successfully gave **{} coins** to <@{}>.".format(amount, id))
                elif amount == 1:
                    embed.add_field(name="Success", value="Successfully gave **{} coin** to <@{}>.".format(amount, id))
                else:
                    embed.add_field(name="Success", value="Successfully took away **{} coins** from <@{}>.".format(abs(amount), id))
                return await ctx.send(embed=embed)
            else:
                embed = botembed("Economy")
                embed.add_field(name="Timeout", value="Confirmation timed out. Please run the command again.")
                return await message.edit(embed=embed)

    @commands.command()
    async def set(self, ctx, user=None, amount=None):
        if ctx.message.author.id != 424991711564136448:
            return
        if user is None:
            id = ctx.message.author.id
        else:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to set their coins.")
                return await ctx.send(embed=embed)
            else:
                if ctx.message.mentions[0].bot:
                    embed = botembed("Economy")
                    embed.add_field(name="Error", value="Invalid parameter - you can't set a bot's coins!")
                    return await ctx.send(embed=embed)
                id = ctx.message.mentions[0].id
        

        if amount is None:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins not specified.")
            return await ctx.send(embed=embed)
        

        try:
            amount = int(amount)
        except:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        else:
            valid, message = await self.confirmation(ctx)
            if valid:
                await message.delete()
                with open(join("economy.json")) as f:
                    data = json.load(f)
                    data[str(id)] = amount
                    with open(join("economy.json"), "w") as nf:
                        json.dump(data, nf)
                embed = botembed("Economy")
                embed.add_field(name="Success", value="Successfully set the coins of <@{}> to **{} coin{}**.".format(id, amount, "s" if amount != 1 else ""))
                return await ctx.send(embed=embed)
            else:
                embed = botembed("Economy")
                embed.add_field(name="Timeout", value="Confirmation timed out. Please run the command again.")
                return await message.edit(embed=embed)

    @commands.command()
    async def pay(self, ctx, user=None, amount=None):
        if user is None:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - mention a user to give coins to.")
            return await ctx.send(embed=embed)
        else:
            if len(ctx.message.mentions) == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - mention a user to give coins to.")
                return await ctx.send(embed=embed)
            else:
                if ctx.message.mentions[0].bot:
                    embed = botembed("Economy")
                    embed.add_field(name="Error", value="Invalid parameter - you can't give coins to a bot!")
                    return await ctx.send(embed=embed)
                id = ctx.message.mentions[0].id
        
        if id == ctx.message.author.id:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - paying yourself with your own money isn't exacty getting you anywhere...")
            return await ctx.send(embed=embed)
        if amount is None:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins not specified.")
            return await ctx.send(embed=embed)
        

        try:
            amount = int(amount)
        except:
            embed = botembed("Economy")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        else:
            if amount == 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - you can't give 0 coins to someone!")
                return await ctx.send(embed=embed)
            elif amount < 0:
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - you can't pay someone negative coins!")
                return await ctx.send(embed=embed)
            elif amount > read_coins(ctx.message.author.id):
                embed = botembed("Economy")
                embed.add_field(name="Error", value="Invalid parameter - you can't afford this payment! Please check your current balance before using this command.")
                return await ctx.send(embed=embed)
            valid, message = await self.confirmation(ctx)
            if valid:
                await message.delete()
                add_coins(id, amount)
                add_coins(ctx.message.author.id, 0-amount)
                
                embed = botembed("Economy")
                if amount > 1:
                    embed.add_field(name="Success", value="You paid <@{}> **{} coins**.".format(id, amount))
                elif amount == 1:
                    embed.add_field(name="Success", value="You paid <@{}> **{} coin**.".format(id, amount))
                await ctx.send(embed=embed)
                try:
                    embed = botembed("Economy")
                    embed.add_field(name="Payment recieved!", value="You recieved **{} coin{}** from {}#{}".format(amount, ("s" if amount > 1 else ""), ctx.message.author.name, ctx.message.author.discriminator))
                    member = discord.utils.find(lambda m: m.id == id, ctx.message.channel.guild.members)
                    await member.send(embed=embed)
                except:
                    return
            else:
                embed = botembed("Economy")
                embed.add_field(name="Timeout", value="Confirmation timed out. Please run the command again.")
                return await message.edit(embed=embed)

    @commands.command()
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        amount = 100
        add_coins(ctx.message.author.id, amount)
        embed = botembed("Economy")
        embed.add_field(name="Daily coins recieved!", value="You recieved your **{} daily coins**. Come back tomorrow for more!".format(amount))
        return await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Economy(bot))