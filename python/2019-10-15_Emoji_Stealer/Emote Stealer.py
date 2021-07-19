import os, sys
import shutil

def clear():
    os.system("clear")

clear()
directory = os.path.dirname(os.path.realpath(__file__))

os.chdir(directory)

print("Setting up...")
try:
    os.mkdir(directory + "/Servers")
except FileExistsError:
    shutil.rmtree(directory + "/Servers")
    os.mkdir(directory + "/Servers")

serverdir = directory + "/Servers"
os.chdir(serverdir)

import discord

client = discord.Client()
clear()

print("Logging in...")

@client.event
async def on_ready():
    serverlen = len(client.guilds)
    s = 0
    for server in client.guilds:
        s += 1
        def serverprint():
            print("Stealing emotes from: ")
            print(server.name + " (Server {}/{})".format(s, serverlen))
        name = server.name.replace("/", "-")
        try:
            os.mkdir(serverdir + "/" + name)
        except FileExistsError:
            shutil.rmtree(serverdir + "/" + name)
            os.mkdir(serverdir + "/" + name)
        emojidir = serverdir + "/" + name
        emojilen = len(server.emojis)
        e = 0
        for emoji in server.emojis:
            e += 1
            clear()
            serverprint()
            ename = emoji.name.replace("/", "-")
            print("Saving emoji:")
            print(":{}: (Emoji {}/{})".format(ename, e, emojilen))
            
            asset = emoji.url
            if emoji.animated:
                await asset.save(emojidir + "/" + ename + ".gif")
            else:
                await asset.save(emojidir + "/" + ename)
    os.chdir(serverdir)
    directories = [x[0] for x in os.walk(serverdir)]
    directories.remove(serverdir)
    clear()
    for dir in directories:
        clear()
        print("Cleaning up: " + dir)
        if not os.listdir(dir):
            shutil.rmtree(dir)
    from webptojpg import convert
    directories = [x[0] for x in os.walk(serverdir)]
    directories.remove(serverdir)
    for dir in directories:
        clear()
        print("Converting all emojis in: \n" + dir)
        convert(dir)
    print("Done")
    for _ in range(5):
        sys.exit(0)
        


token = "[REDACTED]"

client.run(token, bot=False)