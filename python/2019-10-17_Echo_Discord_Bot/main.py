# --- Local File Imports ---
from settings import *


# --- Environment Imports ---
import os
import sys
import random
import asyncio
from math import acos, asin, atan, atan2, ceil, cos, cosh, degrees, e, exp, fabs, floor, fmod, frexp, hypot, ldexp, log, log10, modf, pi, pow, radians, sin, sinh, sqrt, tan, tanh
from urllib.parse import urlencode
from urllib.request import urlopen
import contextlib
import resource
import time
import datetime
import json
import io
import string


# --- Custom Imports ---
import discord
from discord.ext import commands
import requests
import praw
import wikipedia as wp
import js2py


# --- Global Declarations ---
global redditclient
redditclient = praw.Reddit(client_id='[REDACTED]',
                           client_secret='[REDACTED]',
                           user_agent='[REDACTED]')


# --- Code ---
bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")

localdir = os.path.dirname(os.path.realpath(__file__))
with open(localdir + "/starttime.txt", "r") as f:
    start = float(f.read().strip())

#raise KeyboardInterrupt

os.system("clear")


@bot.event
async def on_ready():
    print("Ready")


@bot.event
async def on_message(message):
    try:
        await bot.process_commands(message)
    except Exception as e:
        pass


@bot.command()
async def echo(ctx, *message):
    if len(message) < 1:
        return await ctx.send("Please specify a message to echo.")
    message = " ".join(message)
    await ctx.channel.send(message)


@bot.command()
async def js(ctx, *code):
    if len(code) < 1:
        return await ctx.send("Please enter some code.")
    code = " ".join(code)
    code = code.strip()
    #code = code.replace("\"", "'")
    #code = code.replace("document.write", "return")
    javascript = """var output = "";
document = {
    write: function(value) {
        output = output + value + \"\\
\"
    }
}
""" + code
    #javascript = "".join([c for c in javascript if c in string.printable])

    try:
        context = js2py.EvalJs()
        context.execute(javascript)
        result = context.output.strip()
    except Exception as e:
        return await ctx.send("Error executing code: " + str(e))
    await ctx.send("Code executed. Result: `{}`".format(result))
    #result = ctx.eval(code.replace("document.write", "return "))
    # print ctx.eval(js.replace("document.write", "return "))


@bot.command()
async def cascade(ctx, *message):
    if len(message) < 1:
        return await ctx.send("Please specify a message to cascade.")
    message = " ".join(message)
    if "@everyone" in message:
        return
    newmsg = ""
    for pos in range(len(message)):
        if message[pos] != " ":
            newmsg += message[:pos+1] + "\n"
    try:
        await ctx.channel.send(newmsg)
    except:
        return await ctx.send("Cannot cascade message (message too long)")


@bot.command()
async def help(ctx):
    path = os.path.dirname(os.path.realpath(__file__)) + "/help.txt"
    with open(path, "r") as f:
        helptext = f.read()
    helptext = "```" + helptext + "```"
    user = bot.get_user(ctx.message.author.id)
    dmchannel = await user.create_dm()
    await dmchannel.send(helptext)
    await ctx.channel.send("A help message has been sent, please check your DMs.")


@bot.command(aliases=["btc"])
async def bitcoin(ctx, amount=1):
    response = requests.get("https://api.coinmarketcap.com/v1/ticker/bitcoin/")
    response_json = response.json()
    price = response_json[0]["price_usd"]
    price = str(amount * round(float(price), 2))
    if len(price.split(".")[1]) == 1:
        price = price + "0"
    await ctx.send("The price of **{}** Bitcoin is approximately **{}** USD.".format(amount, price))


@bot.command()
async def morse(ctx, method=None, *message):
    if method is None:
        return await ctx.send("Please specify a method.")
    if len(message) < 1:
        return await ctx.send("Please specify a message to encode/decode.")
    method = method.lower()
    message = " ".join(message)
    morsecode = {'A': '.-', 'B': '-...',
                 'C': '-.-.', 'D': '-..', 'E': '.',
                 'F': '..-.', 'G': '--.', 'H': '....',
                 'I': '..', 'J': '.---', 'K': '-.-',
                 'L': '.-..', 'M': '--', 'N': '-.',
                 'O': '---', 'P': '.--.', 'Q': '--.-',
                 'R': '.-.', 'S': '...', 'T': '-',
                 'U': '..-', 'V': '...-', 'W': '.--',
                 'X': '-..-', 'Y': '-.--', 'Z': '--..',
                 '1': '.----', '2': '..---', '3': '...--',
                 '4': '....-', '5': '.....', '6': '-....',
                 '7': '--...', '8': '---..', '9': '----.',
                 '0': '-----', ',': '--..--', '.': '.-.-.-',
                 '?': '..--..', '/': '-..-.', '-': '-....-',
                 '(': '-.--.', ')': '-.--.-', ":": "---...", "=": "-...-", "+": ".-.-.", "_": "..--.-"}
    if method == "encode":
        try:
            message = message.upper()
            cipher = ''
            for letter in message:
                if letter != ' ':
                    cipher += morsecode[letter] + '/'
                else:
                    cipher += '//'
            if cipher.endswith("//"):
                cipher = cipher[:-2]
            elif cipher.endswith("/"):
                cipher = cipher[:-1]
            cipher = cipher.replace("///", "//")
            message = message.lower()
            return await ctx.send("Input message: **{}**\nOutput message: **{}**".format(message, cipher))
        except:
            return await ctx.send("Invalid message passed.")
    elif method == "decode":
        try:
            if message.endswith("//"):
                message = message[:-2]
            elif message.endswith("/"):
                message = message[:-1]
            words = message.split("//")
            letters = []
            for word in words:
                wletters = word.split("/")
                letters.append(wletters)
            cipher = []
            decodedmorse = dict([(value, key)
                                 for key, value in morsecode.items()])
            for word in letters:
                newword = []
                for letter in word:
                    newword.append(decodedmorse[letter])
                cipher.append("".join(newword))
            cipher = " ".join(cipher)
            cipher = cipher.lower()
            return await ctx.send("Input message: **{}**\nOutput message: **{}**".format(message, cipher))
        except Exception as e:
            print(str(e))
            return await ctx.send("Invalid message passed.")
    else:
        return await ctx.send("Invalid method passed.")


@bot.command()
async def rate(ctx, *item):
    if len(item) < 1:
        return await ctx.send("Please specify something to rate.")
    item = (" ".join(item)).lower()
    with open(localdir + "/rate.json", "r") as f:
        rates = json.load(f)
    if item in rates.keys():
        rating = rates[item]
    else:
        rating = random.randint(0, 10)
        rates[item] = rating
    with open(localdir + "/rate.json", "w") as f:
        json.dump(rates, f)
    message = "Input: **{}**\nResponse: I'd give **{}** a **{}/10**.".format(
        item, item, rating)
    await ctx.send(message)


@bot.command()
async def tag(ctx, method=None, tag=None, value=None):
    if method is None and tag is None and value is None:
        return await ctx.send("Please check the usage using .help")
    if method.lower() == 'view':
        if tag is None:
            return await ctx.send("Please specify a tag to use.")
        with open(localdir + "/tag.json") as f:
            tags = json.load(f)
        if tag not in tags.keys():
            return await ctx.send("Tag not found in tags.")
        message = "Input tag: **{}**\nTag value: {}".format(tag, tags[tag])
        return await ctx.send(message)
    elif method.lower() == "set":
        if tag is None:
            return await ctx.send("Please specify a tag to use.")
        if value is None:
            return await ctx.send("Please specify a value for the tag to use.")
        with open(localdir + "/tag.json") as f:
            tags = json.load(f)
        if tag in tags.keys():
            return await ctx.send("Tag already has set value.")
        tags[tag] = value
        with open(localdir + "/tag.json", "w") as f:
            json.dump(tags, f)
        return await ctx.send("Tag **{}** set with a value of **{}**".format(tag, value))
    else:
        return await ctx.send("Invalid parameters specified.")


@bot.command()
async def wikipedia(ctx, *search_term):
    if len(search_term) < 1:
        return await ctx.send("Please specify a search term.")
    search_term = " ".join(search_term)
    try:
        response = wp.summary(search_term, sentences=2)
    except:
        return await ctx.send("Please give a more specific search term.")
    url = wp.page(search_term).url
    message = "Search term: **{}**\nWikipedia summary: **{}**\nLink: **{}**".format(
        search_term, response, url)
    return await ctx.send(message)


@bot.command(aliases=['lovecalculator'])
async def ship(ctx, person1=None, person2=None):
    if person1 is None and person2 is None:
        return await ctx.send("Please specify two people to ship.")
    if person1 is not None and person2 is None:
        person2 = ctx.message.author.name
    person1 = person1.lower()
    person2 = person2.lower()
    with open(localdir + "/ship.json", 'r') as f:
        ships = json.load(f)
    percentage = random.randint(0, 100)
    if person1 not in ships.keys():
        ships[person1] = {}
        ships[person1][person2] = percentage
        if person2 not in ships.keys():
            ships[person2] = {}
        ships[person2][person1] = percentage
    else:
        if person2 not in ships[person1].keys():
            ships[person1][person2] = percentage
            if person2 not in ships.keys():
                ships[person2] = {}
            ships[person2][person1] = percentage
        else:
            percentage = ships[person1][person2]
    await ctx.send("Input names: **{}** and **{}**\nPercentage: **{}%**".format(person1, person2, percentage))
    with open(localdir + "/ship.json", 'w') as f:
        json.dump(ships, f)


@bot.command(aliases=['eval'])
async def evaluate(ctx, *expression):
    if len(expression) < 1:
        return await ctx.send("Please specify a string to evaluate.")
    expression = " ".join(expression)

    whitelist = ['acos', 'asin', 'atan', 'atan2', 'ceil', 'cos',
                 'cosh', 'degrees', 'e', 'exp', 'fabs', 'floor',
                 'fmod', 'frexp', 'hypot', 'ldexp', 'log', 'log10',
                 'modf', 'pi', 'pow', 'radians', 'sin', 'sinh', 'sqrt',
                 'tan', 'tanh']
    safe_dict = dict([(k, locals().get(k, None)) for k in whitelist])

    try:
        value = eval(expression, {"__builtins__": None}, safe_dict)
    except Exception as e:
        message = "Error evaluating **{}**: **{}**".format(expression, str(e))
    else:
        message = "Input expression: **{}**\nOutput value: **{}**".format(
            expression, value)
    await ctx.send(message)


def isadmin(member):
    return member.guild_permissions.administrator


@bot.command()
async def avatar(ctx, id=None):
    if id is None:
        user = ctx.message.author
    else:
        id = id.replace("<@", "")
        id = id.replace("!", "")
        id = id.replace(">", "")
        try:
            id = int(id)
        except:
            return await ctx.send("Invalid ID passed.")
        else:
            try:
                user = bot.get_user(id)
            except:
                return await ctx.send("Invalid ID passed.")

    avatar = user.avatar_url
    if id is None:
        return await ctx.send("Here's your avatar: {}".format(avatar))
    else:
        return await ctx.send("Heres the avatar for {}#{}: {}".format(user.name, user.discriminator, avatar))


@bot.command()
async def checkadmin(ctx, id=None):
    if id is None:
        member = ctx.message.author
    else:
        id = id.replace("<", "")
        id = id.replace(">", "")
        id = id.replace("@", "")
        try:
            id = int(id)
        except:
            return await ctx.send("Invalid ID passed: {}".format(id))
        member = discord.utils.find(
            lambda m: m.id == int(id), ctx.guild.members)
        if member is None:
            return await ctx.send("User with an ID of {} not found on this server.".format(id))
    admincheck = isadmin(member)
    if id is None:
        if admincheck:
            return await ctx.send("You **are** an admin.")
        else:
            return await ctx.send("You **are not** an admin.")
    else:
        if admincheck:
            return await ctx.send("<@{}> **is** an admin.".format(id))
        else:
            return await ctx.send("<@{}> **is not** an admin.".format(id))


@bot.command()
async def ping(ctx):
    pingtime = round(bot.latency * 1000, 3)
    dt = time.time() - start
    uptime = str(datetime.timedelta(seconds=dt)).split(":")
    uptime = uptime[0] + ":" + uptime[1] + \
        ":" + str(round(float(uptime[2]), 3))
    kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memoryusage = str(round(kb / 1024, 2))
    message = "Ping time: **{}** ms\nUptime: **{}**\nMemory usage: **{}** MB".format(
        pingtime, uptime, memoryusage)
    await ctx.send(message)


@bot.command(aliases=['dice'])
async def roll(ctx, sides=None):
    if sides is None:
        sides = 6
    if "d" in str(sides).lower():
        sides = sides.lower().replace("d", "")
    try:
        sides = int(sides)
    except:
        return await ctx.send("Invalid number of sides passed.")
    if sides < 1:
        return await ctx.send("Invalid number of sides passed.")
    diceroll = random.randint(1, sides)
    message = "Dice: **d{}**\nRoll: **{}**".format(sides, diceroll)
    await ctx.send(message)


@bot.command()
async def xkcd(ctx, givennum=None):
    link = "https://www.xkcd.com"
    f = urlopen(link)
    myfile = f.read().decode("utf-8").split("\n")
    mylines = [line for line in myfile if line.startswith("<meta ")]
    for line in mylines:
        if "og:url" in line:
            _, number = line.split('content="https://xkcd.com/')
            number = number[:-3]
            break
    number = int(number)
    if givennum is None:
        newnumber = random.randint(0, number)
        newurl = "https://www.xkcd.com/" + str(newnumber)
        return await ctx.send("Random XKCD strip: **{}**".format(newurl))
    else:
        try:
            givennum = int(givennum)
        except:
            return await ctx.send("Invalid number passed.")
        if givennum > number or givennum < 0:
            newnumber = number
        else:
            newnumber = givennum
        newurl = "https://www.xkcd.com/" + str(newnumber)
        return await ctx.send("XKCD strip: **{}**".format(newurl))


@bot.command(aliases=["8ball"])
async def magic8ball(ctx, *question):
    if len(question) < 1:
        return await ctx.send("Please specify a question.")
    question = (" ".join(question)).lower()
    with open(localdir + "/8ball.json", "r") as f:
        data = json.load(f)
    if question not in data.keys():
        answers = ["It is certain.",
                   "It is decidedly so.",
                   "Without a doubt.",
                   "Yes - definitely.",
                   "You may rely on it.",
                   "Reply hazy, try again.",
                   "Ask again later.",
                   "Better not tell you now.",
                   "Cannot predict now.",
                   "Concentrate and ask again.",
                   "Don't count on it.",
                   "My reply is no.",
                   "My sources say no.",
                   "Outlook not so good.",
                   "Very doubtful."]
        reply = random.choice(answers)
        data[question] = reply
        with open(localdir + "/8ball.json", "w") as f:
            json.dump(data, f)
    else:
        reply = data[question]
    await ctx.send("Question: **{}**\nReply: **{}**".format(question, reply))


@bot.command()
async def kill(ctx):
    # USE ONLY WITH THE INTENTION OF FIXING A BUG AND BRINGING IT BACK UP ONCE IT IS FIXED
    if ctx.message.author.id != 424991711564136448:
        pass
    else:
        for _ in range(3):
            raise KeyboardInterrupt


@bot.command()
async def tinyurl(ctx, url=None):
    if url is None:
        return await ctx.send("Please specify a URL to shorten.")
    request_url = ("http://tinyurl.com/api-create.php?" +
                   urlencode({'url': url}))
    with contextlib.closing(urlopen(request_url)) as response:
        shortened = response.read().decode('utf-8')
    message = "Input URL: **{}**\nOutput URL: **{}**".format(url, shortened)
    await ctx.send(message)


@bot.command()
async def meme(ctx):
    try:
        url = redditimg("memes")
        if url is None:
            return await ctx.send("Unable to get image from r/memes.")
        await ctx.send(url)
    except Exception as e:
        return await ctx.send("Error getting image: " + str(e))


@bot.command()
async def reddit(ctx, subreddit=None):
    if subreddit is None:
        return await ctx.send("Please specify a subreddit.")
    try:
        url = redditimg(subreddit)
        if url is None:
            return await ctx.send("Unable to get image from r/{}.".format(subreddit))
        await ctx.send(url)
    except Exception as e:
        return await ctx.send("Error getting image: " + str(e))


def redditimg(subname):
    subreddit = redditclient.subreddit(subname)
    try:
        for _ in subreddit.top(limit=1):
            pass
    except:
        return None

    posts = []
    i = 1
    for post in subreddit.hot(limit=None):
        if i > 50:
            break
        if not post.over_18:
            if not post.is_self:
                posts.append(post)
        i += 1
    if len(posts) < 1:
        return None
    keep_choosing = True
    blacklist = []
    while keep_choosing:
        post = random.choice(posts)
        if post in blacklist:
            goodposts = [p for p in posts if not p.over_18]
            if len(goodposts) == 0:
                return None
            continue
        if not post.over_18:
            keep_choosing = False
            break
        blacklist.append(post)
    return post.url


@bot.command()
async def addemoji(ctx, name=None, url=None):
    if not ctx.message.author.guild_permissions.manage_emojis:
        return await ctx.send("You do not have permission to run this command.")
    if name is None:
        return await ctx.send("Please specify a name for the emoji.")
    if url is None:
        return await ctx.send("Please specify an image URL for emoji :{}:.".format(name))
    try:
        resp = requests.get(url)
        image = resp.content
        await ctx.guild.create_custom_emoji(name=name, image=image)
    except Exception as e:
        await ctx.send("Error creating emoji: " + str(e))
    else:
        emoji = discord.utils.find(lambda e: e.name == name, ctx.guild.emojis)
        await ctx.send("Successfully created <:" + str(name) + ":" + str(emoji.id) + ">")

token = "[REDACTED]"
try:
    bot.run(token)
except KeyboardInterrupt:
    import sys
    sys.exit(0)
