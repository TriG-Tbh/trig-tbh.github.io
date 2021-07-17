import t_savefile
import t_care
import sys
from time import sleep
t = t_savefile
c = t_care
confirm = "n"
action = ""

if t.pet_1 == "" and t.pet_2 == "" and t.pet_3 == "":
	print("Welcome to the wonderful world of Tagsugotchi!")
	sleep(2)
	print("Tagsugotchi are little online friends that you can take care of.")
	sleep(2)
	print("It appears you do not yet have a Tagsugotchi.")
	sleep(2)
	print("So, here is your first Tagsugotchi. Take good care of it!")
	sleep(3)
	while len(t.pet_1) == 0 or confirm != "y":
		t.pet_1 = raw_input("Please enter a name for your Tagsugotchi: ")
		if len(t.pet_1) == 0:
			print("Please enter a real name for your Tagsugotchi!")
			sleep(0.5)
		else:
			confirm = raw_input("(y/n) Are you happy with naming your Tagsugotchi \"" + t.pet_1 + "\"? ")
			confirm.lower()
	print("Good job! You now have a Tagsugotchi named \"" + t.pet_1	+ "\"!")
	f = open('t_savefile.py', 'a')
	f.write("pet_1 = \"" + t.pet_1 + "\"")
	f.write("water = 100\n")
	f.write("food = 100\n")
	f.write("cleaning_supplies = 100\n")
	f.write("p1_hapiness = 100\n")
	f.write("p1_hunger = 100\n")
	f.write("p1_thirst = 100\n")
	f.write("p1_sanitation = 100\n")
	f.write("p1_status = \"Happy\"\n")
	f.write("p1_current_action = \"Idle\"\n")
	f.write("p1_level = 1\n")
	f.write("p1_xp = 0\n")
	f.close()
	sleep(2)
	print("Please refer to the documentation file for commands. Take care of your Tagsugotchi!")
	sleep(2)
	sys.exit(0)
else:
	print("Welcome back to Tagsugotchi!")
action = raw_input(">")
if action == "clean":
	c.clean()
