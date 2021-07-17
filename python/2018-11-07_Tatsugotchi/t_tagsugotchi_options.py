from time import sleep
import t_savefile

t = t_savefile

def open_options():
	while True:
		import t_savefile
		option = input("Which Tagsugotchi would you like to open options for?\n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"4) New Tagsugotchi \n"
		"Please select an option (1-3), or \"exit\" to exit: ")
		if option == "exit":
			break
		if option == 4:
			if t.pet_1 == "":
				confirm = input("(Y/N) You currently have " + t.t_bucks + " T-Bucks. Would you like to purchase a new Tagsugotchi for 200 T-Bucks (you cannot take this action back)? ")
				confirm.lower()
				if confirm == "y":
					if t.t_bucks > 199:
						confirm = "n"
						while t.pet_1 == "" or confirm == "n":
							t.pet_1 = input("Please enter a name for your Tatsugotchi: ")
							if t.pet == "":
								print("Please enter a real name!")
								sleep(1)
							else:
								confirm = input("Are you happy with naming your Tagsugotchi \"" + t.pet_1 + "\"? ")
						print("You have successfully purchased \"" + t.pet_1 + "\".")
						save = open("t_savefile", "a")
						save.write("pet_1 = " + t.pet_1)
						save.write("p1_happiness = 100")
					else:
						print("You do not have enough T-Bucks!")
						sleep(1)
				print("Purchase cancelled.")
			elif t.pet_2 == "":
			elif t.pet_3 == "":
			else:
				print("You already have the maximum amount of Tagsugotchi!")

			
