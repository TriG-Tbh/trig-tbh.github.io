import discord
from discord.ext import commands
import urllib.request
import urllib.parse
import re
import pafy
import datetime

def search(term):
    query = term.replace(' ', '_')
    import urllib.request
    import urllib.parse
    import re
    query_string = urllib.parse.urlencode({"search_query" : query})
    html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
    search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
    return search_results

def helpmessage(prefix):
    embed = youtubeembed()
    embed.add_field(name="**Prefix**", value="{}y-".format(prefix))
    embed.add_field(name="**{}y-search <search term>**".format(prefix), value="Searches YouTube for a search term and returns the first results")
    embed.add_field(name="**{}y-video/vid <video link/ID>**".format(prefix), value="Searches YouTube for a search term and returns the first results")
    return embed
    
    



def youtubeembed():
    return discord.Embed(title="YouTube", color=0xff0000)

class Youtube(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['y-search'])
    async def getvideos(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = youtubeembed()
            embed.add_field(name="**Error Message**", value="Please specify a search term.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)
        results = search(searchterm)
        limit = 5
        newresults = []
        i = 1
        for result in results:
            if i > 0:
                newresults.append(result)
            i *= -1
        results = newresults.copy()
        message = ""
        
        message = message.strip()
        embed = youtubeembed()
        embed.add_field(name="**Search Term**", value=searchterm)
        #print(searchterm + "\n\n")
        #print(message)
        i = 1
        #print(results)
        for result in results:
            #print(results)
            video = pafy.new(result)
            author = video.author
            title = video.title
            line = "{}: [{}]({}) by `{}`\n".format(i, title, "https://www.youtube.com/watch?v=" + result, author)
            message += line
            i += 1
        embed.add_field(name="**Search Results**", value=message)
        await ctx.send(embed=embed)

    @commands.command(aliases=['y-video', 'y-vid'])
    async def getvideo(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = youtubeembed()
            embed.add_field(name="**Error Message**", value="Please specify a link/ID.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)

        try:
            video = pafy.new(searchterm)
        except:
            embed = youtubeembed()
            embed.add_field(name="**Error Message**", value="Invalid link/ID passed.")
            return await ctx.send(embed=embed)
        #video = pafy.new(video)
        title = video.title
        author = video.author
        views = video.viewcount
        link = "[{}]({} \"{}\")".format(title, "https://www.youtube.com/watch?v=" + video.videoid, title)
        time = str(datetime.timedelta(seconds=video.length))

        embed = youtubeembed()
        embed.add_field(name="**Title**", value=title)
        embed.add_field(name="**Author**", value=author)
        embed.add_field(name="**Views**", value=views)
        embed.add_field(name="**Likes/Dislikes**", value="{} / {} ({}%)".format(video.likes, video.dislikes, round(video.likes/(video.likes + video.dislikes), 4) * 100))
        embed.add_field(name="**Length**", value=time)
        embed.add_field(name="**Link**", value=link)
        
        embed.set_image(url=video.bigthumbhd)
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Youtube(bot))
