import discord
from discord.ext import commands
import cogs.functions as functions
import cogs.mongohelper as mh

def botembed(description):
    embed = functions.embed("💰 Economy", color=0xffd700)
    embed.description = description
    return embed

    
class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.balances = mh.database["Balances"]

    


    async def process_user(self, user):
        balance = mh.find(self.balances, str(user.id))
        if balance is None:
            mh.update(self.balances, str(user.id), {"balance": "0"})

    async def get_balance(self, user):
        await self.process_user(user)
        balance = mh.find(self.balances, str(user.id))["balance"]
        return int(balance)

    @commands.cooldown(1.0, 86400.0, type=commands.BucketType.user)
    @commands.command()
    async def daily(self, ctx):
        balance = await self.get_balance(ctx.author)
        balance += 100
        mh.update(self.balances, str(ctx.author.id), {"balance": str(balance)})
        embed = botembed("✅ $100 has been added to your balance!")
        await ctx.send(embed=embed)

    @commands.cooldown(1.0, 10.0, type=commands.BucketType.user)
    @commands.command(aliases=['bal'])
    async def balance(self, ctx, user: discord.User=None):
        if user is None:
            user = ctx.author
        await self.process_user(user)
        balance = await self.get_balance(user)
        aoran = "s" if balance != 1 else ""
        embed = botembed(f"🔢 Balance: {balance} coin{aoran}")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Economy(bot))