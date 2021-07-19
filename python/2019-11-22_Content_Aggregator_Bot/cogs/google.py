import discord
from discord.ext import commands
from googlesearch import search
import bs4
import urllib

def googleembed():
    return discord.Embed(title="Google", color=0xffffff - 1)

def helpmessage(prefix):
    embed = googleembed()
    embed.add_field(name="**Prefix**", value="{}g-".format(prefix))
    embed.add_field(name="**{}g-search <search term>**".format(prefix), value="Searches Google for a search term and returns the first results")
    return embed

class Google(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['g-search'])
    async def googlesearch(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = googleembed()
            embed.add_field(name="**Error Message**", value="Please specify a search term.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)
        i = 0
        links = []
        for link in search(searchterm):
            links.append(link)
            i += 1
            if i == 10:
                break
        message = ""
        limit = 3
        if len(links) > limit:
            links = links[:limit]
        i = 1
        for link in links:
            try:
                soup = bs4.BeautifulSoup(urllib.request.urlopen(link), features="html.parser")
                title = soup.title.string
                message += "{}: [{}]({} \"{}\")\n".format(i, title, link, title)
                i += 1
            except:
                pass
        embed = googleembed()
        embed.add_field(name="**Search Term**", value=searchterm)
        embed.add_field(name="**Results**", value=message)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Google(bot))