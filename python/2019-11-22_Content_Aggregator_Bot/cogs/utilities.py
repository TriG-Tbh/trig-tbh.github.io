import discord
from discord.ext import commands
import contextlib
from urllib.request import urlopen
from urllib.parse import urlencode
import requests

def utembed():
    embed = discord.Embed(title="Utilities", color=0xdcdcdc)
    return embed

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['u-tinurl', 'u-shorten'])
    async def shortenurl(self, ctx, url=None):
        if url is None:
            embed = utembed()
            embed.add_field(name="**Error Message**", value="No URL specified to shorten")
            return await ctx.send(embed=embed)
        request_url = ("http://tinyurl.com/api-create.php?" + urlencode({'url': url}))
        try:
            with contextlib.closing(urlopen(request_url)) as response:
                shortened = response.read().decode("utf-8")
        except:
            embed = utembed()
            embed.add_field(name="**Error Message**", value="Invalid URL specified to shorten")
            return await ctx.send(embed=embed)
        embed = utembed()
        embed.add_field(name="**Shortened URL**", value="Old URL: {}\nNew URL: {}".format(url, shortened))
        return await ctx.send(embed=embed)

    @commands.command(aliases=['u-bitcoin', 'u-btc'])
    async def bitcoinprince(self, ctx, amount="1"):
        try:
            amount = int(amount)
        except:
            embed = utembed()
            embed.add_field(name="**Error Message**, value="Invalid amount specified")
            return await ctx.send(embed=embed)
        try:
            response = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
        except:
            embed = utembed()
            embed.add_field(name="**Error Message**", value="Cannot get Bitcoin price - please try again later")
            return await ctx.send(embed=embed)
        response_json = response.json()
        price = response_json[0]["price_usd"]
        price = str(amount * round(float(price), 2))
        if len(price.split(".")[1]) == 1:
            price = price + "0"
        embed = utembed()
        


def setup(bot):
    bot.add_cog(Utilities(bot))