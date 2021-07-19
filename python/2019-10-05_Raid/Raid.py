import os
import discord
import time

os.system("clear")

client = discord.Client()

@client.event
async def on_ready():
	for server in client.guilds:
		#serverid = input("Server ID: ")
		#print(server)
		#print(server.channels)
		#print(client.user.id in [member.id for member in server.members])
		os.system("clear")
		input("Server {} found. Press enter to begin raid. ".format(server.name))
		members = server.members
		memberlen = len(members)
		channels = server.channels
		channelnum = len(channels)
		index = 0
		memberindex = 0
		channelindex = 0
		now = time.time()
		while True:
			try:
				server = client.get_guild(server.id)
			except:
				input("Banned in " + str(time.time() - now) + " seconds. Press enter to continue. ")
				break
			try:
				await channels[channelindex].send("<@" + str(members[memberindex].id) + ">")
			except Exception as e:
				print(channels[channelindex])
				#input(str(e))
				index += 1
				channelindex = index % channelnum
			else:
				index += 1
				channelindex = index % channelnum
				memberindex = index % memberlen

token = "[REDACTED]"
client.run(token, bot=False)