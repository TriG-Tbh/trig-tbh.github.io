import discord
from discord.ext import commands
import wikipedia as wp


def wpembed():
    return discord.Embed(title="Wikipedia", color=0xffffff - 1)

def helpmessage(prefix):
    embed = wpembed()
    embed.add_field(name="**Prefix**", value="{}w-".format(prefix))
    embed.add_field(name="**{}w-search <search term>**".format(prefix), value="Searches Wikipedia for a search term and returns the first results")
    embed.add_field(name="**{}w-summary/sum <search term>**".format(prefix), value="Searches Wikipedia for an article using the given search term and a short summary")
    return embed    

class WpSearch(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['w-search'])
    async def wikisearch(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = wpembed()
            embed.add_field(name="**Error Message**", value="Please specify a search term.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)
        results = wp.search(searchterm)
        if len(results) < 1:
            embed = wpembed()
            embed.add_field(name="**Error Message**", value="Search term \"{}\" did not return any results.".format(searchterm))
            return await ctx.send(embed=embed)
        embed = wpembed()
        embed.add_field(name="**Search Term**", value=searchterm)
        message = "**{}** may refer to...\n\n".format(searchterm)
        i = 1
        for result in results:
            message += "{}: {}\n".format(i, result)
            i += 1
        embed.add_field(name="**Results**", value=message)
        await ctx.send(embed=embed)

    @commands.command(aliases=['w-summary', 'w-sum'])
    async def wpsummary(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = wpembed()
            embed.add_field(name="**Error Message**", value="Please specify a search term.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)
        try:
            summary = wp.summary(searchterm, sentences=3)
        except wp.DisambiguationError as e:
            embed = wpembed()
            message = "Search could not be completed as **{}** may refer to...\n\n".format(searchterm)
            i = 1
            if len(e.options) < 1:
                embed = wpembed()
                embed.add_field(name="**Error Message**", value="Search term \"{}\" did not return any results.".format(searchterm))
                return await ctx.send(embed=embed)
            for result in e.options:
                message += "{}: {}\n".format(i, result)
                i += 1
            embed.add_field(name="**Error Message**", value=message)
            return await ctx.send(embed=embed)
        
        embed = wpembed()
        embed.add_field(name="**Search Term**", value=searchterm)
        embed.add_field(name="**Summary**", value=summary)
        site = wp.page(searchterm)
        embed.add_field(name="**Link**", value="[{}]({} \"{}\")".format(site.title, site.url, site.title))
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(WpSearch(bot))