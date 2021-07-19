import discord
from discord.ext import commands

import random
import json
import os
import asyncio

def join(name):
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), name)

def helpembed(prefix):
    embed = botembed("Help (Gambling)")
    embed.add_field(name="{}slots [bet, default set to 1]".format(prefix), value="Bet coins using slots. Two of a kind pays double the amount betted, three of a kind pays triple, three diamonds pays 5 times.")
    embed.add_field(name="{}dice [bet, default set to 1] <1-6>".format(prefix), value="Rolls a single 6-sided die. Guessing the correct roll pays triple the amount betted.")
    embed.add_field(name="{}coinflip [bet, default set to 1] <heads/tails>".format(prefix), value="Flips a single coin. Choosing the correct side pays double the amount betted.")
    return embed


def botembed(title):
    embed = discord.Embed(color=random.randint(0, 0xffffff))
    embed.set_author(name=title)
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

class Gambling(commands.Cog):
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

    @commands.command()
    async def slots(self, ctx, bet="1"):
        try:
            bet = int(bet)
        except:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        
        if bet < 1:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you must bet at least 1 coin.")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) is None:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="You have no coins. Start talking to get coins!")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) < bet:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you can't afford this gamble! Please check your current balance before using this command.")
            return await ctx.send(embed=embed)

        add_coins(ctx.message.author.id, 0-bet)

        slots = {          
            1: ":lemon:",
            2: ":apple:",
            3: ":banana:",
            4: ":watermelon:",
            5: ":grapes:",
            6: ":strawberry:",
            7: ":cherries:",
            8: ":kiwi:",
            9: ":gem:",
            10: ":pineapple:"
        }
        
        currentslots = []
        for _ in range(3):
            currentslots.append(slots[random.randint(1, 10)])

        embed = botembed("Gambling")
        embed.add_field(name="Slots", value="\n{} : {} : {}".format(currentslots[0], currentslots[1], currentslots[2]))
        message = await ctx.send(embed=embed)
        await asyncio.sleep(1)
        for _ in range(2):
            currentslots = []
            for _ in range(3):
                currentslots.append(slots[random.randint(1, 10)])

            embed = botembed("Gambling")
            embed.add_field(name="Slots", value="\n{} : {} : {}".format(currentslots[0], currentslots[1], currentslots[2]))
            await message.edit(embed=embed)
            await asyncio.sleep(1)
        
        score = 0
        if currentslots[0] == currentslots[1] and currentslots[1] == currentslots[2]:
            if currentslots[0] == ":gem:":
                score = 5 * bet
            else:
                score = 3 * bet
        elif currentslots[0] == currentslots[1] or currentslots[1] == currentslots[2] or currentslots[2] == currentslots[0]:
            score = 2 * bet
        else:
            score = 0
        
        embed = botembed("Gambling")
        embed.add_field(name="Slots", value="\n{} : {} : {}".format(currentslots[0], currentslots[1], currentslots[2]))
        outcome = ""
        if score != 0:
            outcome = "WIN"
        else:
            outcome = "LOSE"
        
        add_coins(ctx.message.author.id, score)

        embed.add_field(name="Outcome: {}".format(outcome), value="You bet **{} coin{}** and won **{} coin{}**.".format(bet, ("s" if bet > 1 else ""), score, ("" if score == 1 else "s")))
        return await message.edit(embed=embed)


    @commands.command()
    async def dice(self, ctx, bet=1, choice=None):
        if choice is None:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - choose a number between 1 and 6.")
            return await ctx.send(embed=embed)
        try:
            choice = int(choice)
        except:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - choice cannot be converted to integer.")
            return await ctx.send(embed=embed)
        
        if choice > 6 or choice < 1:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - choose a number between 1 and 6.")
            return await ctx.send(embed=embed)
        try:
            bet = int(bet)
        except:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        
        if bet < 1:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you must bet at least 1 coin.")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) is None:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="You have no coins. Start talking to get coins!")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) < bet:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you can't afford this gamble! Please check your current balance before using this command.")
            return await ctx.send(embed=embed)

        add_coins(ctx.message.author.id, 0-bet)

        embed = botembed("Gambling")
        embed.add_field(name="Please wait", value="Rolling...")
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        roll = random.randint(1, 6)
        score = 0
        if roll == choice:
            score = 3 * bet
        add_coins(ctx.message.author.id, score)
        embed = botembed("Gambling")
        outcome = "WIN" if roll == choice else "LOSE"

        embed.add_field(name="Outcome: {}".format(outcome), value="You chose {}. \nThe dice rolled {}. \nYou bet **{} coin{}** and won **{} coin{}**.".format(choice, roll, bet, ("" if bet == 1 else "s"), score, ("" if score == 1 else "s")))
        return await message.edit(embed=embed)

    @commands.command(aliases=['flip'])
    async def coinflip(self, ctx, bet=1, choice=None):
        if choice is None:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - choose either `heads` or `tails`.")
            return await ctx.send(embed=embed)

        choice = choice.lower()
        if choice not in ['heads', 'tails']:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - choose either `heads` or `tails`.")
            return await ctx.send(embed=embed)

        
        try:
            bet = int(bet)
        except:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - amount of coins cannot be converted to integer.")
            return await ctx.send(embed=embed)
        
        if bet < 1:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you must bet at least 1 coin.")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) is None:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="You have no coins. Start talking to get coins!")
            return await ctx.send(embed=embed)

        if read_coins(ctx.message.author.id) < bet:
            embed = botembed("Gambling")
            embed.add_field(name="Error", value="Invalid parameter - you can't afford this gamble! Please check your current balance before using this command.")
            return await ctx.send(embed=embed)

        add_coins(ctx.message.author.id, 0-bet)

        embed = botembed("Gambling")
        embed.add_field(name="Please wait", value="Flipping...")
        message = await ctx.send(embed=embed)
        await asyncio.sleep(3)
        flip = random.choice(['heads', 'tails'])
        score = 0
        if flip == choice:
            score = 2 * bet
        add_coins(ctx.message.author.id, score)
        embed = botembed("Gambling")
        outcome = "WIN" if flip == choice else "LOSE"

        embed.add_field(name="Outcome: {}".format(outcome), value="You chose {}. \nThe coin landed with {} facing upwards. \nYou bet **{} coin{}** and won **{} coin{}**.".format(choice, flip, bet, ("" if bet == 1 else "s"), score, ("" if score == 1 else "s")))
        return await message.edit(embed=embed)

def setup(bot):
    bot.add_cog(Gambling(bot))