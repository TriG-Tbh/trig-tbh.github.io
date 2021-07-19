# Setting Discord Status Remotely (SDSR)

import discord
import os
import datetime

client = discord.Client()

@client.event
async def on_ready():
    while True:
        os.system("cls")
        import time
        name = input("Name of activity: ")
        state = input("Current state: ")
        details = input("Activity details: ")
        piurl = input("Primary image URL: ")
        pitext = input("Primary image text: ")
        siurl = input("Secondary image URL: ")
        sitext = input("Secondary image text: ")
        start = time.time()
        activity = discord.Activity(
            type=discord.ActivityType.playing, 
            name=name,
            state=state,
            details=details,
            assets={
                "large_image": piurl,
                "large_text": pitext,
                "small_image": siurl,
                "small_text": sitext
            },
            timestamps={
                "start": start
            })
        await client.change_presence(activity=activity)
        input("Successfully changed status. Press enter to continue. ")

TOKEN = "[REDACTED]"

client.run(TOKEN, bot=False)