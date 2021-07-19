import datetime
import time
import VA_Commands as c

tens, ones = str(datetime.datetime.time(datetime.datetime.now()))[0], str(datetime.datetime.time(datetime.datetime.now()))[1]
hours = str(tens + ones)
hours = int(hours)
if hours >= 0 and hours <= 5:
	print("Good morning.")

if hours >= 6 and hours <= 11:
	print("Good morning.")

if hours >= 12 and hours <= 16:
	print("Good afternoon.")
if hours >= 17 and hours <= 23:
	print("Good evening.")
currenttime = str(time.strftime("%I:%M:%S"))
if hours > 12:
	currenttime += " PM"
print("The current time is " + currenttime)
print("Today's date is " + time.strftime("%x"))

import vlc

while True:
	command = input(" > ")
	if command.startswith("!search "):
		query = command.replace("!search ", "")
		c.search(query)

	if command.startswith("!video "):
		query = command.replace("!video ", "")
		c.play(query, video=True)

	if command.startswith("!music "):
		query = command.replace("!music ", "")
		c.play(query)

	if command.startswith("!stop"):
		c.stopplaying()
		
	if command.startswith("!pause"):
		c.pause()
		
	if command.startswith("!resume"):
		c.resume()

	if command.startswith("!google "):
		query = command.replace("!google ", "")
		c.googlesearch(query)

	if command.startswith("!eval "):
		query = command.replace("!eval ", "")
		c.evaluate(query)

	if command.startswith("!wra "):
		query = command.replace("!wra ", "")
		c.wolframalpha(query)
