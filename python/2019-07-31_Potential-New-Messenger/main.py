import os, sys
pwd = os.getenv("PASSWORD")
os.system("clear")
password = input("Password: ")
if password != pwd:
	sys.exit(0)

import discord
import time
os.system("clear")

client = discord.Client()

async def sendmsg(channel):
	while True:
		os.system("clear")
		statusmsg = ""
		if channel.type == discord.ChannelType.private:
			user = channel.recipient
			for server in client.guilds:
				recipient = discord.utils.find(lambda u: u.name == user.name, server.members)
				if recipient == None:
					pass
				else:
				    break
			if recipient.status == discord.Status.online:
				color = "\u001b[32;1m"
				status = "Online"
			elif recipient.status == discord.Status.offline:
				color = "\u001b[33;1m"
				status = "Idle"
			elif recipient.status == discord.Status.dnd:
				color = "\u001b[31;1m"
				status = "Do Not Disturb"
			elif recipient.status == discord.Status.offline:
				color = "\u001b[0m"
				status = "Offline"
			statusmsg = " (" + color + status + "\u001b[0m" + ")"
		try:
			print("Now chatting on: " + channel.name)
		except AttributeError:
			print("Now chatting on: " + str(channel) + statusmsg)
		messages = await channel.history(limit=25).flatten()
		for i in range(len(messages)):
			i = i + 1
			message = messages[-i]
			content = message.content
			for user in message.mentions:
				content = content.replace(user.mention, "@" + user.name)
			print(message.author.name + ": " + content)
			for attachment in message.attachments:
				print(attachment.url)
		sending = input("> ")
		if sending == "!exit":
			break
		elif sending.startswith("!ban"):
			if channel.type != discord.ChannelType.private and channel.type != discord.ChannelType.group:
				os.system("clear")
				server = input("Server name: ")
				server = discord.utils.find(lambda s: server.lower() in s.name.lower(), client.guilds)
				if server == None:
					input("Server not found. Press enter to continue")
					os.system("clear")
				else:
					os.system("clear")
					print("Server found. Name: " + server.name)
					name = input("User name: ")
					user = discord.utils.find(lambda u: name.lower() in u.name.lower(), server.members)
					if user == None:
						input("User not found. Press enter to continue")
						os.system("clear")
					else:
						# /\/\/\ IMPLEMENT BAN /\/\/\
						os.system("clear")
						print("Banning is not yet supported, come back later!")
						
		elif (sending != "") and (sending != (" " * len(sending))):
			try:
				await channel.send(sending)
			except:
				os.system("clear")
				print("Error sending message")
			else:
				os.system("clear")

@client.event
async def on_ready():
	server = client.get_guild(270352971642961920)
	while True:
		action = input("1: Access DM\n2: Access channel (server -> channel)\n> ")
		if action == "1":
			while True:
				os.system("clear")
				name = input("Name of DM: ")
				channel = discord.utils.find(lambda c: name.lower() in str(c).lower(), client.private_channels)
				if channel == None:
					print("No channel found")
					menu = input("> ")
					if menu == "!exit":
						break
				else:
					await sendmsg(channel)
					break
		elif action == "2":
			while True:
				os.system("clear")
				name = input("Name of server: ")
				server = discord.utils.find(lambda s: name.lower() in s.name.lower(), client.guilds)
				if server == None:
					print("No server found")
					menu = input("> ")
					if menu == "!exit":
						break
				else:
					print("Found server. Name: " + server.name)
					name = input("Name of channel: ")
					channel = discord.utils.find(lambda c: name.lower() in c.name.lower(), server.channels)
					if channel == None:
						print("No channel found")
						menu = input("> ")
						if menu == "!exit":
							break
					else:
						await sendmsg(channel)
						break

token = os.getenv("TOKEN1")
client.run(token, bot=False)