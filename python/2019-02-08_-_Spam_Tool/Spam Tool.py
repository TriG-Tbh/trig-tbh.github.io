from time import sleep
try:
	from pynput.keyboard import Key, Controller
	from random import randint

	# WARNING: This tool will not work unless you have installed the Pynput module AND Python 2.7.15.
	# This tool is used to spam a given phrase any amount of times.
	# The tool can be set to spam a given amount of times, or infinitely.
	# Each selection has a programmable delay between phrases.
	# One possible use for this is on Discord servers with the MEE6 bot.
	# The bot gives users XP every time they type a message (once a minute).
	# This tool can help users grind XP quickly without ever having to use their keyboard.
	# Note: Don't activate this on your friends. They will be very mad.
	# (unless you want to lol)

	keyboard = Controller()
	
	action = 0
	while action != 1 and action != 2:
		action = input("Please type 1 for controlled spamming, or 2 for infinite spamming: ")
	
	string = raw_input("Please type the string you want to be typed: ")  

	if action == 1:
		repeat_times = input("Please type in the amount of times you want the string to be typed: ")

	delay = 0
	while delay < 1 or type(delay) != int:
		delay = input("Please type the delay between phrases (in seconds, 0 is highly unstable): ")
		if delay < 1:
			print("Please make the delay at least 1!")
			sleep(1)
		if type(delay) != int:
			print("Please make the delay a whole number!")
			sleep(1)

	print("Estimated spamming time (in seconds):")
	sleep(1)
	if action == 1:
		time = delay * repeat_times
	else:
		time = "Forever (or until the program is stopped)"
	print(str(time))
	sleep(1)

	print("The spam tool will activate in 3 seconds.")
	sleep(3)

	keyboard.press(Key.enter)
	keyboard.release(Key.enter)

	if action == 1:
		for i in range(1, repeat_times):
			sleep(delay)
			keyboard.type(string)
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)
	elif action == 2:
		while True:
			sleep(delay)
			keyboard.type(string)
			keyboard.press(Key.enter)
			keyboard.release(Key.enter)
	
			
except ImportError:
	print("Error: you might be missing the Pynput module. \n"
	"This module is essential for the Spam Tool. \n"
	"Redirecting to link...")
	import webbrowser
	webbrowser.open('https://pypi.org/project/pynput/#files')
except NameError:
	print("You most likely typed in a string where an integer was required. \n"
	"Please refrain from doing this.")

