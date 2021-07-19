import discord
import time
import notify2

client = discord.Client()

@client.event
async def on_ready():
    print("Ready.")
    while True:
        user = [u for u in client.get_all_members() if u.id == "[REDACTED]"][0]
        if str(user.status) != "Offline":
            notify2.init("Online Indicator")
            n = notify2.Notification(None)
            n.set_urgency(notify2.URGENCY_NORMAL) 
            n.update("GO ON [REDACTED]", "[REDACTED] IS ONLINE")
            n.show()
        time.sleep(60)
        

token = "[REDACTED]"
client.run(token, bot=False)