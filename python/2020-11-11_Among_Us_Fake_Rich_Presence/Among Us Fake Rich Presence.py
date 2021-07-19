# Setting Discord Status Remotely (SDSR)

import discord
import os
import datetime

client = discord.Client()

@client.event
async def on_ready():
    import time
    start = time.time()
    while True:
        os.system("cls")
        command = input("Command: ").strip().lstrip().lower()
        name = "Among Us"
        if command.startswith("imp"):
            state = "Alive (Impostor)"
            details = "In Game"
            sitext = "In Game"
            siurl = "https://i.pinimg.com/originals/a0/4d/c8/a04dc80196748cf4a885f53104626bda.jpg"
        
        elif command.startswith("crewmate"):
            state = "Alive (Crewmate)"
            details = "In Game"
            sitext = "In Game"
            siurl = "https://i.pinimg.com/originals/a0/4d/c8/a04dc80196748cf4a885f53104626bda.jpg"
        
        elif command.startswith("dead"):
            state = state.replace("Alive", "Dead")
        elif command.startswith("lobby"):
            state = "Idle"
            details = "In a Lobby"
            sitext = "In a Lobby"
            siurl = "https://i.pinimg.com/originals/a0/4d/c8/a04dc80196748cf4a885f53104626bda.jpg"
        
        elif command.startswith("idle"):
            state = "Idle"
            details = "Idle"
            sitext = "Idle"
            siurl = "https://www.solidbackgrounds.com/images/1920x1080/1920x1080-amber-orange-solid-color-background.jpg"
        pitext = "Among Us"
        piurl = "default"
        
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

TOKEN = "mfa.odxvYMlplp8hPGaKRCPzliMIF0TK-c91oWNswhWTNhvQ97jYUEmmWRZs_dsVplEA60zG4rj3L1Od5GUthy3S"

client.run(TOKEN, bot=False)