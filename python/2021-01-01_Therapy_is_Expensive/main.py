import discord
from discord.ext import commands
import re
import random
import os
import glob
from difflib import SequenceMatcher
import json
import asyncio

def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()

bot = commands.Bot(command_prefix=".")

basefolder = os.path.dirname(os.path.realpath(__file__))

def load_character(path):
    with open(path) as f:
        return json.load(f)

sessions = {}

class Character:
    def __init__(self, c):
        self.reflections = c["reflections"]
        self.greetings = c["greetings"]
        self.psychobabble = [
            [r"I need (.*)", []],
            [r"Why don\"?t you ([^\?]*)\??", []],
            [r"Why can\"?t I ([^\?]*)\??", []],
            [r"I can\"?t (.*)", []],
            [r"I am (.*)", []],
            [r"I\"?m (.*)", []],
            [r"Are you ([^\?]*)\??", []],
            [r"What (.*)", []],
            [r"How (.*)", []],
            [r"Because (.*)", []],
            [r"(.*) sorry (.*)", []],
            [r"I think (.*)", []],
            [r"(.*) friend (.*)", []],
            [r"Yes", []],
            [r"Is it (.*)", []],
            [r"It is (.*)", []],
            [r"Can you ([^\?]*)\??", []],
            [r"Can I ([^\?]*)\??", []],
            [r"You are (.*)", []],
            [r"You\"?re (.*)", []],
            [r"I don\"?t (.*)", []],
            [r"I feel (.*)", []],
            [r"I have (.*)", []],
            [r"I would (.*)", []],
            [r"Is there (.*)", []],
            [r"My (.*)", []],
            [r"You (.*)", []],
            [r"Why (.*)", []],
            [r"I want (.*)", []],
            [r"(.*)\?", []],
            [r"quit", []],
            [r"(.*)", []]
        ]
        for key in list(c.keys())[3:]:
            self.psychobabble[int(key)] = c[key]


    def reflect(self, fragment):
        tokens = fragment.lower().split()
        for i, token in enumerate(tokens):
            if token in self.reflections:
                tokens[i] = self.reflections[token]
        return " ".join(tokens)

    def respond(self, statement):
        for pattern, responses in self.psychobabble:
            match = re.match(pattern, statement.rstrip(".!"))
            if match:
                response = random.choice(responses)
                return response.format(*[reflect(g) for g in match.groups()])
    

def search(name):
    os.chdir(os.path.join(basefolder, "Characters"))
    options = {}
    for file in glob.glob("*.json"):
        character = {}
        if file == "blank.json": continue
        character["path"] = os.path.join(os.path.join(basefolder, "Characters"), file)
        c = load_character(character["path"])
        character["name"] = c["name"]
        options[similar(c["name"], name)] = character
    return options[sorted(options)[-1]]


@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    if message.channel.id in list(sessions.keys()):
        text = message.content
        await asyncio.sleep(0.075 * len(text))
        async with message.channel.typing():
            c = sessions[message.channel.id]
            response = c.respond(text)
            await asyncio.sleep(0.14 * len(response))
            return await message.channel.send(response)
    else:
        await bot.process_commands(message)


@bot.command()
async def start(ctx, name=None):
    if name is None:
        return
    c = search(name)
    sessions[ctx.channel.id] = Character(c)
    
    


