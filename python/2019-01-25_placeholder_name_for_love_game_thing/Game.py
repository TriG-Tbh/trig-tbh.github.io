from time import sleep
import instance
i = instance
class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
if i.instance == 0:
	print(bcolors.HEADER + 'Welcome.')
	sleep(2.5)
	print("We've been expecting you.")
	sleep(4)
	print("You might not know who we are, but we have been watching you for a very long time.")
	sleep(6)
	print("We are so grateful you have decided to join the beta testing program.")
	sleep(5)
	print("The game you will be testing is one that we've been working on for a while now.")
	sleep(4)
	print("It is, by far, the most immersive dating simulator ever created.")
	sleep(2.5)
	print("However, you must agree to playing this game, as it is not for the faint of heart.")
	sleep(4)
	acceptance = raw_input("Are you willing to play this game? " + bcolors.ENDC)
	print(bcolors.HEADER + "It doesn't matter what you chose, the ")
	
