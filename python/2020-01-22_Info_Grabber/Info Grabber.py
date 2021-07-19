import discord
client = discord.Client()

@client.event
async def on_ready():
    print("Ready")
    server = client.get_guild("[REDACTED]")
    #roles = server.roles[::-1]
    #for role in roles:
    #    print(role.name)
    channel = client.get_channel("[REDACTED]")
    print(channel.bitrate)
    members = server.members
    connect = [m for m in members if channel.permissions_for(m).connect and not m.bot]
    speak = [m for m in members if channel.permissions_for(m).speak and not m.bot]
    for member in connect:
        print(member.name)
    print("-"*20)
    for member in speak:
        print(member.name)
    print("Done")

token = "[REDACTED]"
client.run(token, bot=False)