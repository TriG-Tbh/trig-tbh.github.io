import discord
from discord.ext import commands
import bs4
import requests

def imdbembed():
    return discord.Embed(title="IMDb", color=0xf3ce13)

def helpmessage(prefix):
    embed = imdbembed()
    embed.add_field(name="**Prefix**", value="{}i-".format(prefix))
    embed.add_field(name="**{}i-search <search term>**".format(prefix), value="Returns information about a given movie/TV show from IMDb.")
    return embed

class IMDb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['i-search'])
    async def imdbsearch(self, ctx, *searchterm):
        if len(searchterm) < 1:
            embed = imdbembed()
            embed.add_field(name="**Error Message**", value="Please specify a search term.")
            return await ctx.send(embed=embed)
        searchterm = " ".join(searchterm)
        query = searchterm.replace(" ", "_")
        url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(query)
        resp = requests.get(url)
        soup = bs4.BeautifulSoup(resp.content, features='html.parser')
        links = [("https://www.imdb.com" + link["href"]) for link in soup.find_all('a', href=True) if link['href'].startswith("/title/")]
        try:
            link = links[0]
        except:
            embed = imdbembed()
            embed.add_field(name="**Error Message**", value="Could not find a title with the name \"{}\"".format(searchterm))
            return await ctx.send(embed=embed)

        resp = requests.get(link)
        soup = bs4.BeautifulSoup(resp.content, features='html.parser')

        
        title = soup.find('h1')
        title = title.text
        
        try:
            year = soup.find('span', id='titleYear')
            year = (year.text.replace(")", "")).replace("(", "")
        except:
            year = None
        else:
            if year in title:
                title = title.replace("({})".format(year), "")
        
        summary = soup.find('div', class_='summary_text')
        summary = (summary.text).lstrip().strip()
        summary = summary.replace("See full summary »", "[{}]({} \"{}\")".format("See full summary »", url, title))
        pieces = summary.split("\n")
        for piece in pieces:
            if "See full summary\xa0»" in piece:
                s_url = [("https://www.imdb.com" + link["href"]) for link in soup.find_all('a', href=True) if "See full summary" in link.text]
                s_url = s_url[0]
                pieces[pieces.index(piece)] = piece.replace("See full summary\xa0»", "[{}]({} \"{}\")".format("See full summary\xa0»", s_url, title)).lstrip().strip()
        summary = "\n".join(pieces)
        

        rating = soup.find('span', itemprop="ratingValue")
        rating = (rating.text) + " / 10"

        ratings = soup.find('span', itemprop="ratingCount")
        ratings = ratings.text

        rating = rating + " (out of {} ratings)".format(ratings)

        #mpaaratings = [rating for rating in soup.find_all('span') if ("-PG" in rating or ("Rated " in rating and " for " in rating))]
        try:
            if year is None:
                mpaaratings = [r for r in soup.find_all('div', class_='txt-block') if "Certificate:" in r.text]
                mpaarating = mpaaratings[0].text.split("\n")[2]
            else:
                mpaaratings = [r for r in soup.find_all('div', class_='txt-block') if "Motion Picture Rating" in r.text]
                mpaarating = mpaaratings[0].text.split("\n")[4]
        except:
            mpaarating = "None"
        mpaarating = mpaarating.strip()

        time = soup.find('time')
        time = time.text
        if year is None:
            time = time.split("\n")[1].lstrip().strip()
        if "h" in time:
            hours = time.split("h")[0]
            if int(hours) > 1 or int(hours) == 0:
                h_aoran = "s"
            else:
                h_aoran = ""
        if "m" in time:
            if "h" in time:
                minutes = time.split("h")[1].split("min")[0].lstrip()
            else:
                minutes = time.split("min")[0].lstrip()
            if int(minutes) > 1 or int(minutes) == 0:
                m_aoran = "s"
            else:
                m_aoran = ""
        if "h" in time and "m" in time:
            time = time.replace("h", " hour{},".format(h_aoran)).replace("min", " minute{}".format(m_aoran)).lstrip().strip()
        elif "h" in time:
            time = time.replace("h", " hour{},".format(h_aoran)).lstrip().strip()
        elif "m" in time:
            time = time.replace("min", " minute{}".format(m_aoran)).lstrip().strip()

        posterimg = [i for i in soup.find_all("img") if "poster" in str(i.get("alt")).lower()]
        posterimg = posterimg[0].get("src")

        #print(title)
        #print(year)
        #print(time)
        #print(summary)
        #print(rating)
        #print(mpaarating)
        embed = imdbembed()
        embed.add_field(name="**DISCLAIMER**", value="Data from IMDb. I DO NOT OWN ANY OF THE DATA")
        embed.add_field(name="**Title**", value=title)
        embed.add_field(name="**Summary**", value=summary)
        if year is None:
            ftype = "TV Show"
        else:
            ftype = "Movie"
        embed.add_field(name="**Type of Film**", value=ftype)
        if year is not None:
            embed.add_field(name="**Year of Release**", value=year)
        else:
            links = [l for l in soup.find_all("a") if "TV Series (" in l.text]
            runtime = links[0].text.strip()
            runtime = runtime.replace("TV Series (", "").replace(")", "")
            if runtime.endswith(" "):
                runtime = runtime.split("–")[0] + " - " + "Present"
            else:
                runtime = runtime.replace("–", " - ")
            embed.add_field(name="**Years in Production**", value=runtime)
        if year is not None:
            embed.add_field(name="**Runtime**", value=time)
        else:
            embed.add_field(name="**Average Runtime**", value=time)
        embed.add_field(name="**Rating**", value=rating)
        embed.add_field(name="**Parental Rating**", value=mpaarating)
        embed.set_image(url=posterimg)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(IMDb(bot))