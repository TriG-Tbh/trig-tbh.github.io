import discord
from discord.ext import commands
import os
import cogs.settings as settings

bot = commands.Bot(command_prefix=settings.PREFIX)
bot.remove_command("help")

@bot.event
async def on_ready():
    print("Ready")

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)
    if ctx.valid:
        if not isinstance(message.channel, discord.abc.PrivateChannel):
            try:
                await bot.process_commands(message) 
            except Exception as e:
                user = await bot.fetch_user("[REDACTED]")
                await user.send(str(e))

path = os.path.dirname(os.path.realpath(__file__))
cogs = os.path.join(path, "cogs")

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

