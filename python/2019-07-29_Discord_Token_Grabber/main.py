import pkg_resources
pkg_resources.require("discord==0.16.0")
import discord

import os, sys

os.system("clear")

client = discord.Client()

email = input("Email: ")
pwd = input("Password: ")

@client.event
async def on_ready():
    print(client.http.token)

try:
    try:
        client.loop.run_until_complete(client.login(email, pwd))
    except TypeError:
        raise TypeError("This account has 2FA enabled. Good job. If you want your token, ")

except KeyboardInterrupt:
    client.loop.run_until_complete(client.logout())
    # cancel all tasks lingering
finally:
    client.loop.close()