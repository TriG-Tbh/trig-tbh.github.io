import discord
import os
import sys
from discord.ext import commands
import cogs.settings as settings
import cogs.functions as functions
import json
import random
import datetime

path = os.path.dirname(os.path.realpath(__file__))
cogs = os.path.join(path, "cogs")
sys.path.append(os.path.join(path, "cogs"))




class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    async def on_ready(self):
        user = self.user
        print(f"Logged in as: {user.name}#{user.discriminator}")
        await bot.change_presence(activity=discord.Game(name=f"pranks on 1-A", start=datetime.datetime.now()))
    
    def response(self, resp_type):
        options = {
            0: "footer",
            1: "accepted",
            2: "error",
            3: "join",
            4: "leave",
            5: "praise"
        }
        with open(os.path.join(path, "responses.json")) as f:
            responses = json.loads(f.read())
        
        response = random.choice(responses[options[resp_type]])
        return response

    def get_characters(self, number):
        cs = {}
        with open(os.path.join(path, "characters.json")) as f:
            characters = json.loads(f.read())
        number = min(max(0, number), len(characters.keys()))
        
        while True:
            choice = random.choice(list(characters.keys()))
            if choice not in cs.keys():
                cs[choice] = characters[choice]
            if len(cs) == number:
                break

        return cs

bot = Bot(command_prefix=settings.PREFIX)
@bot.command(name="quit")
async def q(ctx):
    import sys
    sys.exit(0)

#print(bot.get_characters(3))

for file in os.listdir(cogs):
    if file.endswith(".py"):
        name = file[:-3]
        with open(os.path.join(cogs, file), encoding="utf-8") as f:
            try:
                content = f.read()
            except:
                print(name)
        if "# DNI" not in content:  # "DNI": Do Not Import
            bot.load_extension("cogs." + name)

try:
    bot.run(settings.TOKEN)
except KeyboardInterrupt:
    import sys
    sys.exit(0)