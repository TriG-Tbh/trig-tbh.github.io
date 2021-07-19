import discord
from discord.ext import commands
import praw
import random
import datetime
import requests
import os


def redditembed():
    return discord.Embed(title="Reddit", color=0xFF5700)

def helpmessage(prefix):
    embed = redditembed()
    embed.add_field(name="**Prefix**", value="{}r-".format(prefix))
    embed.add_field(name="**{}r-search <subreddit>**".format(prefix), value="Returns a random post from a given subreddit")
    embed.add_field(name="**{}r-user <username>**".format(prefix), value="Returns information for a given user")
    embed.add_field(name="**{}r-subreddit/sub <subreddit>**".format(prefix), value="Returns information for a given subreddit")
    embed.add_field(name="**{}r-getpost/id <post link/ID>**".format(prefix), value="Returns information for a given post")
    return embed

def postembed(post):
    title = post.title
    author = post.author
    score = post.score
    url = "https://www.reddit.com" + post.permalink
    method = ""
    if post.is_self:
        method = "Text post"
    else:
        imgurl = post.url
        #print(imgurl)
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
    embed = redditembed()
    embed.add_field(name="**Title**", value=title)
    embed.add_field(name="**Author**", value="u/{}".format(author))
    embed.add_field(name="**Score**", value=score)
    embed.add_field(name="**Comments**", value=comments)
    embed.add_field(name="**NSFW**", value=("Yes" if post.over_18 else "No"))
    embed.add_field(name="**Type**", value=method)
    embed.add_field(name="**URL**", value="[{}]({} \"{}\")".format(title, url, title))
    if method != "Unknown" and method != "Gfycat link" and method != "YouTube link" and not post.is_self and not post.over_18 and method != "Reddit video" and not imgurl.endswith("gifv"):
        embed.set_image(url=imgurl)
    return embed


class Reddit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

    @commands.command(aliases=['r-search'])
    async def randompost(self, ctx, sub=None):
        if sub is None:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Please enter a subreddit to pull a random post from.")
            return await ctx.send(embed=embed)
        try:
            for _ in self.reddit.subreddit(sub).top(limit=1):
                pass
        except:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Subreddit \"r/{}\" does not exist.".format(sub))
            return await ctx.send(embed=embed)
        subreddit = self.reddit.subreddit(sub)
        picks = []
        for post in subreddit.hot(limit=25):
            if post.over_18:
                try:
                    if ctx.channel.is_nsfw():
                        picks.append(post)
                except:
                    continue
            else:
                picks.append(post)
        if len(picks) < 1:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Could not get post from subreddit \"r/{}\".".format(sub))
            return await ctx.send(embed=embed)

        post = random.choice(picks)
        await ctx.send(embed=postembed(post))
        
        

    @commands.command(aliases=['r-user'])
    async def getuser(self, ctx, name=None):
        if name is None:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Please enter a username.")
            return await ctx.send(embed=embed)

        user = self.reddit.redditor(name)
        try:
            _ = user.id
        except:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="User \"u/{}\" does not exist.".format(name))
            return await ctx.send(embed=embed)
        name = "u/" + user.name
        uid = user.id
        is_over_18 = ("Yes" if user.subreddit["over_18"] else "No")
        karma = user.link_karma
        pfp = user.icon_img
        url = "https://www.reddit.com/" + name
        embed = redditembed()
        embed.add_field(name="**Name**", value=name)
        embed.add_field(name="**ID**", value=uid)
        embed.add_field(name="**NSFW**", value=is_over_18)
        embed.add_field(name="**Karma**", value=karma)
        embed.add_field(name="**URL**", value="[{}]({} \"{}\")".format(name, url, name))
        embed.set_thumbnail(url=pfp)
        return await ctx.send(embed=embed)

    @commands.command(aliases=['r-sub', 'r-subreddit'])
    async def getsub(self, ctx, sub):
        if sub is None:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Please enter a subreddit to pull a random post from.")
            return await ctx.send(embed=embed)
        try:
            for _ in self.reddit.subreddit(sub).top(limit=1):
                pass
        except:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Subreddit \"r/{}\" does not exist.".format(sub))
            return await ctx.send(embed=embed)
        subreddit = self.reddit.subreddit(sub)
        name = "r/" + subreddit.display_name
        url = "https://www.reddit.com/r/" + subreddit.display_name
        nsfw = ("Yes" if subreddit.over18 else "No")
        subs = subreddit.subscribers
        created = str(datetime.datetime.fromtimestamp(subreddit.created_utc))
        desc = subreddit.public_description
        embed = redditembed()
        embed.add_field(name="**Subreddit Name**", value=name)
        embed.add_field(name="**Description**", value=desc)
        embed.add_field(name="**Subscribers**", value=subs)
        embed.add_field(name="**Date Created**", value=created)
        embed.add_field(name="**NSFW**", value=nsfw)
        embed.set_thumbnail(url=subreddit.community_icon)
        await ctx.send(embed=embed)


    @commands.command(aliases=['r-getpost', 'r-id'])
    async def getpost(self, ctx, identifier=None):
        if identifier is None:
            embed = redditembed()
            embed.add_field(name="**Error Message**", value="Please enter either the link to a post or the post's ID.")
            return await ctx.send(embed=embed)
        try:
            post = self.reddit.submission(url=identifier)
        except:
            try:
                post = self.reddit.submission(id=identifier)
            except:
                embed = redditembed()
                embed.add_field(name="**Error Message**", value="Invalid link/ID passed.")
                return await ctx.send(embed=embed)
        
        await ctx.send(embed=postembed(post))
        
    

def setup(bot):
    bot.add_cog(Reddit(bot))