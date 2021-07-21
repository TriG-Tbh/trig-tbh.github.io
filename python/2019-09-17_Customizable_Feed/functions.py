import os
import glob
import random
import platform
import emailing
import settings

def clear():
	if platform.system() == "Windows":
		os.system('cls')
	if platform.system() == "Linux":
		os.system("clear")

def gotopath():
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	return dir_path

def load_feed(name):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	exists = False
	for filename in glob.glob("*"):
		if filename == name + ".feed":
			exists = True
			break
	if not exists:
		raise ValueError("feed \"" + name + ".feed\" does not exist")
	else:
		with open(dir_path + "/" + name + '.feed', "r") as f:
			content = f.read()
		content = content.split("\n")
		data = {}
		for line in content:
			feed, posts = line.split(",")
			data[feed] = int(posts)
		return data

def edit_settings():
	import settings
	editing = True
	dir_path = os.path.dirname(os.path.realpath(__file__))
	with open(dir_path + "/" + "settings.py", "r") as f:
		settingscontent = f.read().strip()
	settingscontent = settingscontent.replace("\n\n", "\n")
	settingbools = []
	for line in settingscontent.split("\n"):
		content = line.split(" = ")
		print(content)
		settingbools.append(
			(content[0], str(settings.LIMIT) if content[0].strip() == "LIMIT" else (True if content[1].strip() == "True" else False)))
	while editing:
		clear()
		content = ""
		for i, tup in enumerate(settingbools):
			content += str(i + 1) + ": " + tup[0] + ": " + str(tup[1]) + "\n"
		content = content.strip()
		print(content)
		selection = input("Enter a number to toggle the setting, or \"save\" to save the settings: ")
		selection = selection.strip().lower() 

		try:
			selection = int(selection)
		except:
			if selection != "save":
				input("Selection not valid. Press enter to continue. ")
				continue
			else:
				savecontent = ""
				for tup in settingbools:
					savecontent += tup[0] + " = " + str(tup[1]) + "\n"
				with open(dir_path + "/" + "settings.py", "w") as f:
					f.write(savecontent)
				input("Settings have been saved. Press enter to continue. ")
				break
		if selection == 0:
			input('Selection not valid. Press enter to continue. ')
			continue
		try:
			_ = settingbools[selection - 1]
		except:
			input('Selection not valid. Press enter to continue. ')
			continue
		if settingbools[selection - 1][0] == "LIMIT":
			limit = input("Enter new limit: ")
			try:
				limit = int(limit)
			except:
				input("Limit must be an integer value. Press enter to continue. ")
				continue
			settingbools[selection - 1] = (settingbools[selection - 1][0], limit)
			input("Limit of posts set to " + str(limit) + ". Press enter to continue. ")
			continue

		settingbools[selection - 1] = (
			settingbools[selection - 1][0], not(settingbools[selection - 1][1]))
			
def make_feed(reddit):
	gotopath()
	clear()	
	adding = True
	feed = {}
	while adding:
		clear()
		displaymessage = ""
		for subreddit in feed:
			displaymessage += ("r/" + subreddit + ": " + str(feed[subreddit]) + ("\n" if subreddit != list(feed.keys())[-1] else ""))
		displaymessage = displaymessage.strip()
		if displaymessage:
			print(displaymessage)

		command = input("\nCommands:\n\"add\": add a subreddit to the feed\n\"edit\": edits the amount of posts added from a subreddit\n\"remove\": removes a subreddit from the feed\n\"save\": finishes and saves the feed\nEnter a command: ")
		command = command.strip().lower()
		if command == "add":
			subreddit = input("Enter a subreddit name: r/")
			try:
				for _ in reddit.subreddit(subreddit).hot(limit=1):
					pass # Validates that subreddit exists
			except: 
				input("Subreddit with name \"r/" + subreddit + "\" not found. Press enter to continue. ")
				continue
			else:
				posts = input("Enter a number of posts for the subreddit \"r/" + subreddit + "\": ")
				try:
					posts = int(posts)
				except:
					input("Invalid number \"" + posts + "\". Press enter to continue. ")
				else:
					feed[subreddit] = posts
					input(str(posts) + " posts from \"r/" + subreddit + "\" added to the feed. Press enter to continue. ")
		elif command == "edit":
			subreddit = input("Enter the name of the subreddit: ")
			exists = False
			for subredditname in feed:
				if subreddit == subredditname:
					exists = True
					break
			if not exists:
				input("Subreddit with name \"" + subreddit + "\" not found in feed. Press enter to continue. ")
				continue
			else:
				posts = input(
					"Enter a number of posts for the subreddit \"r/" + subreddit + "\": ")
				try:
					posts = int(posts)
				except:
					input("Invalid number \"" + posts + "\". Press enter to continue. ")
					continue
				else:
					feed[subreddit] = posts
					input("Number of posts from r/" + subreddit + " changed to " + str(posts) + ". Press enter to continue. ")
		elif command == "remove":
			subreddit = input("Enter the name of the subreddit: ")
			exists = False
			for subredditname in feed:
				if subreddit == subredditname:
					exists = True
					break
			if not exists:
				input("Subreddit with name \"" + subreddit +
				      "\" not found in feed. Press enter to continue. ")
				continue
			else:
				del feed[subreddit]
				input("Subreddit r/" + subreddit + " removed from feed. Press enter to continue. ")
		elif command == "save":
			if feed:
				save = input("Would you like to save (Y/N)? ")
				if save.lower().strip().startswith("y"):
					name = input("Name of feed (will be saved as [name].feed): ")
					create_feed(name, feed)
					input("Feed saved to \"" + name + ".feed\". Press enter to continue. ")
					break
				else:
					input("Feed not saved. Press enter to continue. ")
					break
			else:
				print("Feed cannot be empty. Press enter to continue. ")
		else:
			input("Invalid command. Press enter to continue. ")

def edit_feed(reddit):
	gotopath()
	clear()	
	adding = True
	name, feed = select_feed()
	while adding:
		clear()
		displaymessage = ""
		for subreddit in feed:
			displaymessage += "r/" + subreddit + ": " + \
				str(feed[subreddit]) + ("\n" if subreddit != list(feed.keys())[-1] else "")
		displaymessage = displaymessage.strip()
		if displaymessage:
			print(displaymessage)

		command = input("\nCommands:\n\"add\": add a subreddit to the feed\n\"edit\": edits the amount of posts added from a subreddit\n\"remove\": removes a subreddit from the feed\n\"save\": finishes and saves the feed\nEnter a command: ")
		command = command.strip().lower()
		if command == "add":
			subreddit = input("Enter a subreddit name: r/")
			try:
				for _ in reddit.subreddit(subreddit).hot(limit=1):
					pass # Validates that subreddit exists
			except Exception as e:
				print(str(e)) 
				input("Subreddit with name \"r/" + subreddit + "\" not found. Press enter to continue. ")
				continue
			else:
				posts = input("Enter a number of posts for the subreddit \"r/" + subreddit + "\": ")
				try:
					posts = int(posts)
				except:
					input("Invalid number \"" + posts + "\". Press enter to continue. ")
				else:
					feed[subreddit] = posts
					input(str(posts) + " posts from \"r/" + subreddit + "\" added to the feed. Press enter to continue. ")
		elif command == "edit":
			subreddit = input("Enter the name of the subreddit: ")
			exists = False
			for subredditname in feed:
				if subreddit == subredditname:
					exists = True
					break
			if not exists:
				input("Subreddit with name \"" + subreddit + "\" not found in feed. Press enter to continue. ")
				continue
			else:
				posts = input(
					"Enter a number of posts for the subreddit \"r/" + subreddit + "\": ")
				try:
					posts = int(posts)
				except:
					input("Invalid number \"" + posts + "\". Press enter to continue. ")
				else:
					feed[subreddit] = posts
					input("Number of posts from r/" + subreddit + " changed to " + str(posts) + ". Press enter to continue. ")
		elif command == "remove":
			subreddit = input("Enter the name of the subreddit: ")
			exists = False
			for subredditname in feed:
				if subreddit == subredditname:
					exists = True
					break
			if not exists:
				input("Subreddit with name \"" + subreddit +
				      "\" not found in feed. Press enter to continue. ")
				continue
			else:
				del feed[subreddit]
				input("Subreddit r/" + subreddit + " removed from feed. Press enter to continue. ")
		elif command == "save":
			if feed:
				save = input("Would you like to save (Y/N)? ")
				if save.lower().strip().startswith("y"):
					content = []
					dir_path = os.path.dirname(os.path.realpath(__file__))
					for item in feed:
						content.append(item + "," + str(feed[item]))
					content = "\n".join(content)
					with open(dir_path + "/" + name + ".feed", 'w') as f:
						f.write(content)
					input("Edited feed saved to \"" + name + ".feed\". Press enter to continue. ")
					break
				else:
					input("Feed not saved. Press enter to continue. ")
					break
			else:
				input("Feed cannot be empty. Press enter to continue.")
		else:
			input("Invalid command. Press enter to continue. ")

def create_feed(name, data):
	dir_path = os.path.dirname(os.path.realpath(__file__))
	os.chdir(dir_path)
	for filename in glob.glob("*"):
		if filename == name + ".feed":
			name = name + "-1"
			break
	content = []
	for item in data:
		content.append(item + "," + str(data[item]))
	content = "\n".join(content)
	with open(dir_path + "/" + name + ".feed", 'w') as f:
		f.write(content)

def delete_feed():
	gotopath()
	name, _ = select_feed()
	dir_path = os.path.dirname(os.path.realpath(__file__))
	
	os.remove(dir_path + "/" + name + ".feed")
	input("File \"" + name + ".feed\" has been deleted. Press enter to continue. ")

def select_feed():
	while True:
		clear()
		gotopath()
		names = ""
		filenames = []
		i = 1
		for filename in glob.glob("*"):
			if filename.endswith(".feed"):
				names = names + str(i) + ": " + filename + "\n"
				name, _ = filename.split(".")
				filenames.append(name)
				i += 1
		names = names.strip()
		print(names)
		selection = input("Enter a feed number: ")
		try:
			selection = int(selection)
		except:
			input('Selection not valid. Press enter to continue. ')
			continue
		if selection == 0:
			input('Selection not valid. Press enter to continue. ')
			continue
		try:
			selection = filenames[selection - 1]
		except:
			print('Selection not valid. Press enter to continue. ')
			continue
		data = load_feed(selection)
		return selection, data

def send_feed(reddit, name, feed):
	content = ""
	selected = []
	for subredditname in feed:
		content = content + "r/" + subredditname + ": " + str(feed[subredditname]) + "\n"
	content = content + "\n"
	for subredditname in feed:
		posts = []
		subreddit = reddit.subreddit(subredditname)
		for post in subreddit.hot(limit=settings.LIMIT):
			posts.append(post)
		for _ in range(feed[subredditname]):
			if not settings.ALLOW_NSFW:
				nsfw = True
				while nsfw:
					post = random.choice(posts)
					nsfw = post.over_18
					if not nsfw:
						break
			else:
				post = random.choice(posts)
			selected.append(post)
			del posts[posts.index(post)]
	for post in selected:
		content = content + "Post subreddit: r/" + post.subreddit.display_name + "\n"
		if settings.FLAIR_NAME:
			content = content + "Post flair: " + str(post.link_flair_text) + "\n"
		if settings.POST_AUTHOR:
			content = content + "Post author: u/" + post.author.name + "\n"
		content = content + "Post title: " + post.title + "\n"
		content = content + "Post link: https://www.reddit.com" + post.permalink + "\n"
		if settings.PICTURE_LINK:
			if not post.is_self:
				content = content + "Post picture: " + post.url + "\n"
		if settings.POST_SCORE:
			content = content + "Post score: " + str(post.score) + "\n"
		content = content + "\n\n"
	content = content + "Feed curator created by u/TriG-tbh"
	message = input("Enter a message for the recipient (press enter to skip): ")
	if message:
		content = message + "\n\n" + content
	recipient = input("Enter recipient email address: ")
	try:
		emailing.send(name, recipient, content)
	except ValueError:
		print("Invalid recipient email. Press enter to continue. ")
	else:
		input("Email sent. Press enter to continue. ")
	clear()
