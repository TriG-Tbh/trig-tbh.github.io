from time import sleep
import t_savefile
selection = ""
t = t_savefile

def open_options():
	while True:
		import t_savefile
		t = t_savefile
		option = raw_input("Which Tagsugotchi would you like to open options for?\n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"4) New Tagsugotchi \n"
		"Please select an option (1-4), or \"leave\" to exit: ")
		if len(option) == 1:
			option = int(option)
		if option == "leave":
			break
		if option == 1:
			if t.pet_1 != "":
				if t.p1_current_action == "Idle":
					selection = input("What would you like to do with " + t.pet_1 + ": \n"
					"1) Rename (Costs 50 T-Bucks)\n"
					"2) Disown (Costs 100 T-Bucks, plus acceptance of being a soulless person)\n"
					"3) Go back\n"
					"Please select an option: ")
					if selection == 1:
						if t.t_bucks > 49:
							while t.pet_1 == "" or confirm == "n":
								t.pet_1 = raw_input("Please enter a name for your Tatsugotchi: ")
								if t.pet_1 == "":
									print("Please enter a real name!")
									sleep(1)
								else:
									confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_1 + "\"? ")
							print("You have successfully renamed your Tagsugotchi to \"" + t.pet_1 + "\".")
							f = open("t_savefile.py", "a")
							f.write("t_bucks = t_bucks - 50")
							f.write("pet_1 = \"" + t.pet_1 + "\"\n")
							f.close()
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					elif selection == 2:
						if t.t_bucks > 99:
							confirm = raw_input("(Y/N) Are you ABSOLUTELY sure you want to do this? Your Tagsugotchi will be gone, along with their level and XP. Do you want to go through with this? ")
							confirm.lower()
							if confirm != "y":
								confirm = "n"
							if confirm == "y":
								print("You are a heartless human being...")
								sleep(1)
								f = open("t_savefile.py", "a")
								f.write("t_bucks = t_bucks - 100\n")
								f.write("pet_1 = \"\"\n")
								f.write("p1_happiness = 0\n")
								f.write("p1_hunger = 0\n")
								f.write("p1_thirst = 0\n")
								f.write("p1_sanitation = 0\n")
								f.write("p1_status = \"\"\n")
								f.write("p1_current_action = \"\"\n")
								f.write("p1_level = 0\n")
								f.write("p1_xp = 0\n")
								f.close()
								print(t.pet_1 + " has now been disowned.")
								t.pet_1 = ""
								break
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					else:
						print("Your Tagsugotchi must be Idle!")
			else:
				print("Please select one of your Tagsugotchi!")
		elif option == 2:
			if t.pet_2 != "":
				if t.p2_current_action == "Idle":
					selection = input("What would you like to do with " + t.pet_2 + ": \n"
					"1) Rename (Costs 50 T-Bucks)\n"
					"2) Disown (Costs 100 T-Bucks, plus acceptance of being a soulless person)\n"
					"3) Go back\n"
					"Please select an option: ")
					if selection == 1:
						if t.t_bucks > 49:
							while t.pet_2 == "" or confirm == "n":
								t.pet_2 = raw_input("Please enter a name for your Tatsugotchi: ")
								if t.pet_2 == "":
									print("Please enter a real name!")
									sleep(1)
								else:
									confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_2 + "\"? ")
							print("You have successfully renamed your Tagsugotchi to \"" + t.pet_2 + "\".")
							f = open("t_savefile.py", "a")
							f.write("t_bucks = t_bucks - 50")
							f.write("pet_2 = \"" + t.pet_2 + "\"\n")
							f.close()
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					elif selection == 2:
						if t.t_bucks > 99:
							confirm = raw_input("(Y/N) Are you ABSOLUTELY sure you want to do this? Your Tagsugotchi will be gone, along with their level and XP. Do you want to go through with this? ")
							confirm.lower()
							if confirm != "y":
								confirm = "n"
							if confirm == "y":
								print("You are a heartless human being...")
								sleep(1)
								f = open("t_savefile.py", "a")
								f.write("t_bucks = t_bucks - 100\n")
								f.write("pet_2 = \"\"\n")
								f.write("p2_happiness = 0\n")
								f.write("p2_hunger = 0\n")
								f.write("p2_thirst = 0\n")
								f.write("p2_sanitation = 0\n")
								f.write("p2_status = \"\"\n")
								f.write("p2_current_action = \"\"\n")
								f.write("p2_level = 0\n")
								f.write("p2_xp = 0\n")
								f.close()
								print(t.pet_2 + " has now been disowned.")
								t.pet_2 = ""
								break
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					else:
						print("Your Tagsugotchi must be Idle!")
			else:
				print("Please select one of your Tagsugotchi!")
		elif option == 3:
			if t.pet_3 != "":
				if t.p3_current_action == "Idle":
					selection = input("What would you like to do with " + t.pet_3 + ": \n"
					"1) Rename (Costs 50 T-Bucks)\n"
					"2) Disown (Costs 100 T-Bucks, plus acceptance of being a soulless person)\n"
					"3) Go back\n"
					"Please select an option: ")
					if selection == 1:
						if t.t_bucks > 49:
							while t.pet_3 == "" or confirm == "n":
								t.pet_3 = raw_input("Please enter a name for your Tatsugotchi: ")
								if t.pet_3 == "":
									print("Please enter a real name!")
									sleep(1)
								else:
									confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_3 + "\"? ")
							print("You have successfully renamed your Tagsugotchi to \"" + t.pet_3 + "\".")
							f = open("t_savefile.py", "a")
							f.write("t_bucks = t_bucks - 50")
							f.write("pet_2 = \"" + t.pet_3 + "\"\n")
							f.close()
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					elif selection == 2:
						if t.t_bucks > 99:
							confirm = raw_input("(Y/N) Are you ABSOLUTELY sure you want to do this? Your Tagsugotchi will be gone, along with their level and XP. Do you want to go through with this? ")
							confirm.lower()
							if confirm != "y":
								confirm = "n"
							if confirm == "y":
								print("You are a heartless human being...")
								sleep(1)
								f = open("t_savefile.py", "a")
								f.write("t_bucks = t_bucks - 100\n")
								f.write("pet_3 = \"\"\n")
								f.write("p3_happiness = 0\n")
								f.write("p3_hunger = 0\n")
								f.write("p3_thirst = 0\n")
								f.write("p3_sanitation = 0\n")
								f.write("p3_status = \"\"\n")
								f.write("p3_current_action = \"\"\n")
								f.write("p3_level = 0\n")
								f.write("p3_xp = 0\n")
								f.close()
								print(t.pet_3 + " has now been disowned.")
								t.pet_3 = ""
								break
						else:
							print("You do not have enough T-Bucks!")
						sleep(1)
					else:
						print("Your Tagsugotchi must be Idle!")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 4:
			if t.pet_1 == "":
				confirm = raw_input("(Y/N) You currently have " + str(t.t_bucks) + " T-Bucks. Would you like to purchase a new Tagsugotchi for 200 T-Bucks (you cannot take this action back)? ")
				confirm.lower()
				if confirm == "y":
					if t.t_bucks > 199:
						confirm = "n"
						while t.pet_1 == "" or confirm == "n":
							t.pet_1 = raw_input("Please enter a name for your Tatsugotchi: ")
							if t.pet_1 == "":
								print("Please enter a real name!")
								sleep(1)
							else:
								confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_1 + "\"? ")
						print("You have successfully purchased \"" + t.pet_1 + "\".")
						f = open("t_savefile.py", "a")
						f.write("t_bucks = t_bucks - 200\n")
						f.write("pet_1 = \"" + t.pet_1 + "\"\n")
						f.write("p1_happiness = 100\n")
						f.write("p1_hunger = 100\n")
						f.write("p1_thirst = 100\n")
						f.write("p1_sanitation = 100\n")
						f.write("p1_status = \"Happy\"\n")
						f.write("p1_current_action = \"Idle\"\n")
						f.write("p1_level = 1\n")
						f.write("p1_xp = 0\n")
						f.close()
						sleep(1)
					else:
						print("You do not have enough T-Bucks!")
						sleep(1)
				else:
					print("Purchase cancelled.")
					sleep(1)
			elif t.pet_2 == "":
				confirm = raw_input("(Y/N) You currently have " + str(t.t_bucks) + " T-Bucks. Would you like to purchase a new Tagsugotchi for 200 T-Bucks (you cannot take this action back)? ")
				confirm.lower()
				if confirm == "y":
					if t.t_bucks > 199:
						confirm = "n"
						while t.pet_2 == "" or confirm == "n":
							t.pet_2 = raw_input("Please enter a name for your Tatsugotchi: ")
							if t.pet_2 == "":
								print("Please enter a real name!")
								sleep(1)
							else:
								confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_2 + "\"? ")
						print("You have successfully purchased \"" + t.pet_2 + "\".")
						f = open("t_savefile.py", "a")
						f.write("t_bucks = t_bucks - 200\n")
						f.write("pet_2 = \"" + t.pet_2 + "\"\n")
						f.write("p2_happiness = 100\n")
						f.write("p2_hunger = 100\n")
						f.write("p2_thirst = 100\n")
						f.write("p2_sanitation = 100\n")
						f.write("p2_status = \"Happy\"\n")
						f.write("p2_current_action = \"Idle\"\n")
						f.write("p2_level = 1\n")
						f.write("p2_xp = 0\n")
						f.close()
						sleep(1)
					else:
						print("You do not have enough T-Bucks!")
						sleep(1)
				else:
					print("Purchase cancelled.")
					sleep(1)
			elif t.pet_3 == "":
				confirm = raw_input("(Y/N) You currently have " + str(t.t_bucks) + " T-Bucks. Would you like to purchase a new Tagsugotchi for 200 T-Bucks (you cannot take this action back)? ")
				confirm.lower()
				if confirm == "y":
					if t.t_bucks > 199:
						confirm = "n"
						while t.pet_3 == "" or confirm == "n":
							t.pet_3 = raw_input("Please enter a name for your Tatsugotchi: ")
							if t.pet_3 == "":
								print("Please enter a real name!")
								sleep(1)
							else:
								confirm = raw_input("Are you happy with naming your Tagsugotchi \"" + t.pet_3 + "\"? ")
						print("You have successfully purchased \"" + t.pet_3 + "\".")
						f = open("t_savefile.py", "a")
						f.write("t_bucks = t_bucks - 200\n")
						f.write("pet_3 = \"" + t.pet_3 + "\"\n")
						f.write("p3_happiness = 100\n")
						f.write("p3_hunger = 100\n")
						f.write("p3_thirst = 100\n")
						f.write("p3_sanitation = 100\n")
						f.write("p3_status = \"Happy\"\n")
						f.write("p3_current_action = \"Idle\"\n")
						f.write("p3_level = 1\n")
						f.write("p3_xp = 0\n")
						f.close()
						sleep(1)
					else:
						print("You do not have enough T-Bucks!")
						sleep(1)
				else:
					print("Purchase cancelled.")
					sleep(1)
			else:
				print("You already have the maximum amount of Tagsugotchi!")
				sleep(1)

			
