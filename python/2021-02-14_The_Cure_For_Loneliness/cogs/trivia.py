import discord
from discord.ext import commands
import functions
import urllib.request
import random
import json
import asyncio

def botembed(title):
    embed = functions.embed("Trivia - " + title, color=0x8f0000)
    return embed

def error(errormsg):
    embed = functions.error("Trivia", errormsg)
    return embed

url = "https://opentdb.com/api.php?amount=1"

class Trivia(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trivia(self, ctx):
        embed = botembed("Question Asked")
        question = urllib.request.urlopen(url).read().decode(encoding='UTF-8')
        question = question.replace("&quot", "\"").replace("&#039;", "\'")
        question = json.loads(question)["results"][0]
        desc = "❓ {} {}\n".format(self.bot.response(1), random.choice(["I got a good one for you!", "Here's a question!", "Let's see how you do against this!"]))
        desc = desc + "It's a{} `{}` question from the `{}` category.\n```{}{}```\n".format("n" if question["difficulty"][0] == "e" else "", question["difficulty"], question["category"], "T/F: " if question["type"] == "boolean" else "", question["question"])
        
        paired = {}
        reverse = {}
        
        if question["type"] == "boolean":
            desc = desc + "`T`: True\n`F`: False\n"
            paired["t"] = "True"
            paired["f"] = "False"
        else:
            answers = [question["correct_answer"]] + question["incorrect_answers"]
            random.shuffle(answers)
            for a in range(len(answers)):
                desc = desc + "`{}`: {}\n".format("ABCD"[a], answers[a])
                paired["abcd"[a]] = answers[a]
                reverse[answers[a]] = "abcd"[a]
        
        
            
        times = {
            "easy": 10,
            "medium": 15,
            "hard": 20
        }

        desc = desc + "You have `{}` seconds. {}".format(times[question["difficulty"]], random.choice(["You got this!", "I believe in you!", "You can do this!"]))
        embed.description = desc

        message = await ctx.send(embed=embed)

        def check(message):
            if message.author == ctx.message.author and message.channel == ctx.channel:
                content = message.content.strip().lstrip().lower()
                if content[0] in paired.keys():
                    return True
        
        try:
            m = await self.bot.wait_for("message", check=check, timeout=times[question["difficulty"]])
        except asyncio.TimeoutError:
            embed = botembed("Time's Up!")
            embed.description = "❓ Time's up! Unfortunately, you didn't answer the question in time."
            await message.edit(embed=embed)
        else:
            content = m.content.strip().lstrip().lower()
            if paired[content[0]] == question["correct_answer"]:
                embed = botembed("Win")
                embed.description = "You got that {}! {}".format(random.choice(["correct", "right"]), self.bot.response(1))
                return await ctx.send(embed=embed)
            else:
                embed = botembed("Loss")
                embed.description = "{} that wasn't the correct answer.\nThe correct answer was `{}`.".format(self.bot.response(2), question["correct_answer"])
                return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Trivia(bot))