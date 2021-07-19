from discord.ext import commands

import settings
import functions
import requests
import random
import urllib
import contextlib
import requests
import datetime
import json
import pytz

import praw



from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="hello world")

from timezonefinder import TimezoneFinder
tf = TimezoneFinder()

def botembed():
    embed = functions.embed("Utilities", color=0xff00ff)
    return embed

class Utilities(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.redditclient = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

    @commands.command()
    async def bitcoin(self, ctx, amount=1):
        try:
            amount = int(amount)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - amount is not an integer.", inline=False)
            return await ctx.send(embed=embed)
        if amount < 1:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - amount must be greater than 1.", inline=False)
            return await ctx.send(embed=embed)
        try:
            response = requests.get("https://api.coindesk.com/v1/bpi/currentprice.json")
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Cannot get price at this time. Please try again later.", inline=False)
            return await ctx.send(embed=embed)
        response_json = response.json()
        usd = str(response_json["bpi"]["USD"]["rate_float"] * amount)
        gbp = str(response_json["bpi"]["GBP"]["rate_float"] * amount)
        eur = str(response_json["bpi"]["EUR"]["rate_float"] * amount)
        prices = [usd, gbp, eur]
        prices = [str(round(float(amount), 2)) + ("0" if len(amount.split(".")[1]) == 1 else "") for amount in prices]
        embed = botembed()
        embed.add_field(name="Bitcoin Price", value="The price of {} bitcoin is...".format(amount), inline=False)
        embed.add_field(name="USD", value=prices[0], inline=False)
        embed.add_field(name="GBP", value=prices[1], inline=False)
        embed.add_field(name="EUR", value=prices[2], inline=False)
        return await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, sides=6):
        try:
            sides = int(sides)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - amount is not an integer.", inline=False)
            return await ctx.send(embed=embed)
        if sides < 2:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - number of sides must be at least 2.", inline=False)
            return await ctx.send(embed=embed)
        choice = random.randint(1, sides)
        embed = botembed()
        embed.add_field(name="Roll", value="The {}-sided die has landed on {}".format(sides, choice), inline=False)
        return await ctx.send(embed=embed)
    
    @commands.command()
    async def tinyurl(self, ctx, url=None):
        if url is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - URL not specified.", inline=False)
            return await ctx.send(embed=embed)
        try:
            requests.get(url)
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - invalid URL passed.", inline=False)
            return await ctx.send(embed=embed)
        request_url = ("http://tinyurl.com/api-create.php?" + urllib.parse.urlencode({'url': url}))
        try:
            with contextlib.closing(urllib.request.urlopen(request_url)) as response:
                shortened = response.read().decode('utf-8')
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Cannot shorten URL at this time. Please try again later.", inline=False)
            return await ctx.send(embed=embed)
        embed = botembed()
        embed.add_field(name="Shortened URL", value=shortened, inline=False)
        return await ctx.send(embed=embed)

    @commands.command()
    async def avatar(self, ctx, id=None):
        if id is None:
            user = ctx.message.author
        else:
            
            try:
                id = int(id)
            except:
                if len(ctx.message.mentions) == 0:
                    embed = botembed()
                    embed.add_field(name="Error", value="Invalid parameter - invalid ID passed.", inline=False)
                    return await ctx.send(embed=embed)
                else:
                    user = ctx.message.mentions[0]
            else:
                try:
                    user = await self.bot.fetch_user(id)
                except:
                    embed = botembed()
                    embed.add_field(name="Error", value="Invalid parameter - invalid ID passed.", inline=False)
                    return await ctx.send(embed=embed)
        image = str(user.avatar_url_as(static_format="png", size=1024))
        embed = botembed()
        embed.set_image(url=image)
        embed.add_field(name="Avatar", value="Here is the avatar for `{}#{}` (<@{}>):".format(user.name, user.discriminator, user.id), inline=False)
        return await ctx.send(embed=embed)
            
    @commands.command()
    async def time(self, ctx, locationinput):
        try:
            with urllib.request.urlopen("https://nominatim.openstreetmap.org/search/{}?format=json".format(locationinput)) as url:
                data = json.loads(url.read().decode())
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Cannot get location data at this time. Please try again later.", inline=False)
            return await ctx.send(embed=embed)
        if len(data) == 0:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - invalid location passed.", inline=False)
            return await ctx.send(embed=embed)
        location = data[0]
        locationname = location['display_name']
        latitude, longitude = float(location['lat']), float(location['lon'])
        timezone = tf.timezone_at(lng=longitude, lat=latitude)
        dt = datetime.datetime.now(pytz.timezone(timezone))
        day = dt.strftime("%m/%d/%Y")
        time = dt.strftime("%H:%M:%S")
        time12h = dt.strftime("%I:%M:%S %p")
        zone = dt.strftime("%Z%z")
        embed = botembed()
        embed.add_field(name="Location", value=locationname, inline=False)
        embed.add_field(name="Timezone", value=zone, inline=False)
        embed.add_field(name="Day", value=day, inline=False)
        embed.add_field(name="Time (12-hour)", value=time12h, inline=False)
        embed.add_field(name="Time (24-hour)", value=time, inline=False)
        return await ctx.send(embed=embed)
    
    def reddit_post(self, subreddit, image=False, nsfw=False):
        subreddit = self.redditclient.subreddit(subreddit)
        picks = []
        for post in subreddit.hot(limit=25):
            if post.over_18:
                try:
                    if nsfw and image != post.is_self:
                        picks.append(post)
                    elif nsfw and image == False:
                        picks.append(post)
                except:
                    continue
            else:
                if image != post.is_self:
                    picks.append(post)
                elif image == False:
                    picks.append(post)
        if len(picks) < 1:
            return None
        post = random.choice(picks)
        title = post.title
        author = post.author
        score = post.score
        url = "https://www.reddit.com" + post.permalink
        method = ""
        if post.is_self:
            method = "Text post"
        else:
            imgurl = post.url
            if "imgur" in imgurl:
                method = "Imgur file"
            elif "youtu" in imgurl:
                method = "YouTube link"
            elif "v.redd.it" in imgurl:
                method = "Reddit video"
            elif "gfycat" in imgurl:
                method = "Gfycat link"
            elif "redd.it" in imgurl:
                method = "Reddit file"
            else:
                method = "Unknown"
        post.comments.replace_more(limit=None)
        comments = len(post.comments.list())
        embed = botembed()
        embed.add_field(name="Title", value=title, inline=False)
        embed.add_field(name="Author", value="u/{}".format(author), inline=False)
        embed.add_field(name="Score", value=score, inline=False)
        embed.add_field(name="Comments", value=comments, inline=False)
        embed.add_field(name="NSFW", value=("Yes" if post.over_18 else "No"), inline=False)
        embed.add_field(name="Type", value=method, inline=False)
        embed.add_field(name="URL", value="[{}]({} \"{}\")".format(title, url, title), inline=False)
        if method != "Unknown" and method != "Gfycat link" and method != "YouTube link" and not post.is_self and not post.over_18 and method != "Reddit video" and not imgurl.endswith("gifv"):
            embed.set_image(url=imgurl)
        return embed

    @commands.command()
    async def reddit(self, ctx, parameter=None, subreddit=None):
        image = False
        if subreddit is None and parameter is None:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - please specify a subreddit.", inline=False)
            return await ctx.send(embed=embed)
        if parameter is not None and subreddit is None:
            if parameter == "-image":
                embed = botembed()
                embed.add_field(name="Error", value="Invalid parameter - please specify a subreddit.", inline=False)
                return await ctx.send(embed=embed)
            else:
                sub = parameter
        else:
            image = True
            sub = subreddit
        try:
            for _ in self.redditclient.subreddit(sub).top(limit=1):
                pass
        except:
            embed = botembed()
            embed.add_field(name="Error", value="Invalid parameter - subreddit r/{} does not exist".format(sub), inline=False)
            return await ctx.send(embed=embed)
        post = self.reddit_post(sub, image=image, nsfw=ctx.channel.is_nsfw())
        if post is None:
            embed = botembed()
            embed.add_field(name="Error", value="Cannot get post at this time. Please try again later.", inline=False)
            return await ctx.send(embed=embed)
        await ctx.send(embed=post)

    @commands.command()
    async def meme(self, ctx):
        post = self.reddit_post("memes", image=True, nsfw=ctx.channel.is_nsfw())
        if post is None:
            embed = botembed()
            embed.add_field(name="Error", value="Cannot get post at this time. Please try again later.", inline=False)
            return await ctx.send(embed=embed)
        await ctx.send(embed=post)



def setup(bot):
    bot.add_cog(Utilities(bot))