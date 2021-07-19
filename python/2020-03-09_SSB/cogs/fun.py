from discord.ext import commands
import functions
import random

def botembed():
    embed = functions.embed("Fun", color=0x32cd32)
    return embed

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mastermind(self, ctx):
        characters = ["A", "B", "C", "D"]
        code = ""
        for _ in range(5):
            code += random.choice(characters)
        attempts = 10
        embed = botembed()
        embed.add_field(name="Mastermind", value="Enter a 5-character combination, using the characters `A`, `B`, `C` and `D`.", inline=False)
        await ctx.send(embed=embed)
        def check(message):
            if message.author == ctx.message.author:
                if len(message.content) == len(code):
                    for character in message.content.upper().strip():
                        if character not in characters:
                            return False
                    return True
            else:
                return False
        while True:
            if attempts < 1:
                break
            message = await self.bot.wait_for("message", check=check)
            correct = 0
            for pos in range(len(code)):
                if code[pos] == message.content.upper()[pos]:
                    correct += 1
            if correct == len(code):
                embed = botembed()
                embed.add_field(name="You win!", value="The correct code was `{}`. <@{}> has won!".format(code, message.author.id), inline=False)
                return await ctx.send(embed=embed)
            else:
                attempts -= 1
                if attempts >= 1:
                    embed = botembed()
                    embed.add_field(name="Incorrect code", value="{} character{} {} correct. \nYou have {} guess{} remaining.".format(correct, ("s" if correct != 1 else ""), ("were" if correct != 1 else "was"), attempts, ("es" if attempts > 1 else "")), inline=False)
                    await ctx.send(embed=embed)
        embed = botembed()
        embed.add_field(name="You lose!", value="You lose! The correct code was `{}`".format(code), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))