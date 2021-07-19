import discord
import os
import sys
from discord.ext import commands
import cogs.settings as settings

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
       
    async def on_ready(self):
        user = self.user
        print(f"Logged in as: {user.name}#{user.discriminator}")
    

bot = Bot(command_prefix=settings.PREFIX)

path = os.path.dirname(os.path.realpath(__file__))
cogs = os.path.join(path, "cogs")
sys.path.append(os.path.join(path, "cogs"))

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

bot.run(settings.TOKEN)