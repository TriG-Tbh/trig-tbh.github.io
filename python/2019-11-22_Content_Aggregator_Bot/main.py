import discord
from discord.ext import commands
from settings import PREFIX
import os, sys
import resource

dirpath = os.path.dirname(os.path.realpath(__file__))

bot = commands.Bot(command_prefix=PREFIX)
bot.remove_command("help")

def getallcogs():
    return [filename[:-3].lower() for filename in os.listdir(f'{dirpath}/cogs') if filename.endswith(".py")]

@bot.event
async def on_ready():
    print("Ready.")

def generalembed():
    embed = discord.Embed(title="General")
    return embed


def helpmessage():
    embed = generalembed()
    embed.add_field(name="**Syntax**", value="`<variable`: Required\n`[variable]`: Optional\n`.command1/command2`: Both `.command1` and `.command2` have the same result")
    embed.add_field(name="**{}help**".format(PREFIX), value="Displays this message.")
    embed.add_field(name="**{}ping**".format(PREFIX), value="Displays the bot's ping time and memory usage.")
    embed.add_field(name="**{}about**".format(PREFIX), value="Displays information about the bot.")
    embed.add_field(name="**List of Available Cogs**", value="\n".join(["`{}`".format(c) for c in getallcogs()]))
    embed.add_field(name="**Cogs**", value="Yacab runs on modules of commands called \"cogs\". These cogs have different sets of commands.\nTo access the help commands for a cog, enter `{}help <cog name>`\nFor example, to access the help command for the YouTube cogs, enter `{}help youtube`.".format(PREFIX, PREFIX))
    return embed

@bot.event
async def on_message(message):
    content = message.content
    if content.startswith(".help "):
        cogname = content.replace(".help ", "")
        sys.path.insert(1, dirpath + "/cogs")
        cogname = cogname.lower()
        for filename in os.listdir(f"{dirpath}/cogs"):
            name = filename[:-3]
            if filename.endswith(".py") and name == cogname:
                file = __import__(name)
                embed = file.helpmessage(PREFIX)
                
                accepted = True
                try:
                    channel = await message.author.create_dm()
                    await channel.send(embed=embed)
                    break
                except:
                    try:
                        await message.channel.send(embed=embed)
                        accepted = False
                    except:
                        break
                if accepted:
                    if not isinstance(message.channel, discord.abc.PrivateChannel):
                        newembed = generalembed()
                        newembed.add_field(name="**Help Message**", value="You have been sent a help message. Please check your DMs.")
                        await message.channel.send(embed=newembed)
                        break
        else:
            embed = generalembed()
            embed.add_field(name="**Error Message**", value="Cog with name `{}` not found (use `.help` to get a list of cogs)".format(cogname))
            return await message.channel.send(embed=embed)
    else:
        await bot.process_commands(message)
            

@bot.command()
async def about(ctx):
    embed = generalembed()
    user = bot.get_user("[REDACTED]")
    message = """Your Average Content Aggregator Bot (Yacab)
A bot developed by {}#{}
Initial bot developed fully in one weekend
Main purpose: To pull content from the Internet and display it in neat little embeds.
Movie information from IMDb""".format(user.name, user.discriminator)
    embed.add_field(name="**Information**", value=message)
    await ctx.send(embed=embed)


@bot.command()
async def load(ctx, extension=None):
    if ctx.message.author.id == "[REDACTED]":
        if extension is None:
            embed = generalembed()
            embed.add_field(name="**Error Message**", value="Please specify a cog to load (use `.getcogs` to get a list of unloaded cogs).")
            return await ctx.send(embed=embed)
        embed = generalembed()
        try:
            bot.load_extension(f"cogs.{extension}")
        except Exception as e:
            embed.add_field(name="**Error Message**", value="Error loading cog \"{}\": {}".format(extension, str(e)))
        else:
            embed.add_field(name="**Cog Loaded**", value="Successfully loaded cog \"{}\"".format(extension))
        await ctx.send(embed=embed)


@bot.command()
async def unload(ctx, extension=None):
    if ctx.message.author.id == "[REDACTED]":
        if extension is None:
            embed = generalembed()
            embed.add_field(name="**Error Message**", value="Please specify a cog to unload (use `.getcogs` to get a list of loaded cogs).")
            return await ctx.send(embed=embed)
        embed = generalembed()
        try:
            bot.unload_extension(f"cogs.{extension}")
        except Exception as e:
            embed.add_field(name="**Error Message**", value="Error unloading cog \"{}\": **{}**".format(extension, str(e)))
        else:
            embed.add_field(name="**Cog Unloaded**", value="Successfully unloaded cog \"{}\"".format(extension))
        await ctx.send(embed=embed)

@bot.command()
async def cogs(ctx):
    if ctx.message.author.id == "[REDACTED]":
        loadedlist = [c.lower() for c in list(bot.cogs.keys())]
        loaded = "\n".join(loadedlist)
        unloaded = ""
        message = ""
        for cogname in getallcogs():
            if cogname not in loadedlist:
                unloaded += cogname + "\n"
            message += cogname + "\n"
        embed = generalembed()
        embed.add_field(name="**List of Cogs**", value=message)
        if len(loaded.split("\n")) > 1:
            embed.add_field(name="**Loaded Cogs**", value=loaded)
        if len(unloaded.split('\n')) > 1:
            embed.add_field(name="**Unloaded Cogs**", value=unloaded)
        await ctx.send(embed=embed)


@bot.command()
async def ping(ctx):
    embed = generalembed()
    pingtime = round(bot.latency * 1000, 3)
    kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memoryusage = str(round(kb / 1024, 2))
    embed.add_field(name="**Ping Time**", value="{} milliseconds".format(pingtime))
    embed.add_field(name="**Memory Usage**", value="{} MB".format(memoryusage))
    await ctx.send(embed=embed)
    

@bot.command()
async def help(ctx):
    helpembed = helpmessage()
    accepted = True
    try:
        channel = await ctx.message.author.create_dm()
        await channel.send(embed=helpembed)
    except:
        await ctx.send(embed=helpembed)
        accepted = False
    if accepted:
        if not isinstance(ctx.channel, discord.abc.PrivateChannel):
            newembed = generalembed()
            newembed.add_field(name="**Help Message**", value="You have been sent a help message. Please check your DMs.")
            await ctx.send(embed=newembed)



@bot.command()
async def invite(ctx):
    inviteembed = generalembed()
    link = "[REDACTED]"
    inviteembed.add_field(name="**Invite**", value="Want to add Yacab to your own server? Visit [{}]({}) to add it to your server!".format("this link", link))
    await ctx.send(embed=inviteembed)

for filename in os.listdir(f'{dirpath}/cogs'):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")



token = "[REDACTED]"

bot.run(token)