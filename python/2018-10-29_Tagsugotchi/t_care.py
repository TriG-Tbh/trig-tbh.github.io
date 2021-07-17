from time import sleep
import t_savefile
t = t_savefile

t.p1_sanitation = int(t.p1_sanitation)
t.p2_sanitation = int(t.p2_sanitation)
t.p3_sanitation = int(t.p3_sanitation)
t.p1_hunger = int(t.p1_hunger)
t.p2_hunger = int(t.p2_hunger)
t.p3_hunger = int(t.p3_hunger)
t.p1_thirst = int(t.p1_thirst)
t.p2_thirst = int(t.p2_thirst)
t.p3_thirst = int(t.p3_thirst)
t.cleaning_supplies = int(t.cleaning_supplies)
t.food = int(t.food)
t.water = int(t.water)


def clean():
	import t_savefile
	f = open('t_savefile', 'a')
	if t.cleaning_supplies > 9:	
		option = input("Whick Tagsugotchi would you like to clean? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			if t.pet_1 != "":
				if t.p1_current_action == "Idle":
					t.p1_sanitation = t.p1_sanitation + 15
					t.cleaning_supplies = t.cleaning_supplies - 10
					print("You cleaned " + t.pet_1 + "!")
					
					f.write("p1_sanitation = " + str(t.p1_sanitation) + "\n")
					
					f.write("cleaning_supplies = " + str(t.cleaning_supplies) + "\n")
				else:
					print("Your Tagsugotchi must be Idle!")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 2:
			if t.pet_2 != "":
				if t.p2_current_action == "Idle":
					t.p2_sanitation = t.p2_sanitation + 15
					t.cleaning_supplies = t.cleaning_supplies - 10
					print("You cleaned " + t.pet_2 + "!")
					
					f.write("p2_sanitation = " + str(t.p2_sanitation) + "\n")
					
					f.write("cleaning_supplies = " + str(t.cleaning_supplies) + "\n")
				else:
					print("Your Tagsugotchi must be Idle
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 3:
			if t.pet_3 != "":
				t.p3_sanitation = t.p3_sanitation + 15
				t.cleaning_supplies = t.cleaning_supplies - 10
				print("You cleaned " + t.pet_3 + "!")
				
				f.write("p3_sanitation = " + str(t.p3_sanitation) + "\n")
				
				f.write("cleaning_supplies = " + str(t.cleaning_supplies) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
	else:
		print("You do not have enough cleaning supplies! Purchase more in the shop.")
	f.close()
	sleep(1)

def feed():
	import t_savefile
	f = open('t_savefile.py', 'a')
	if t.food > 9:	
		option = input("Whick Tagsugotchi would you like to give food to? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			if t.pet_1 != "":
				t.p1_hunger = t.p1_hunger + 15
				t.food = t.food - 10
				print("You gave food to " + str(t.pet_1) + "!")
				
				f.write("p1_hunger = " + str(t.p1_hunger) + "\n")
				
				f.write("food = " + str(t.food) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 2:
			if t.pet_2 != "":
				t.p2_hunger = t.p2_hunger + 15
				t.food = t.food - 10
				print("You gave food to " + str(t.pet_2) + "!")
				
				f.write("p2_hunger = " + str(t.p2_hunger) + "\n")
				
				f.write("food = " + str(t.food) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 3:
			if t.pet_3 != "":
				t.p3_hunger = t.p3_hunger + 15
				t.food = t.food - 10
				print("You gave food to " + str(t.pet_3) + "!")
				
				f.write("p3_hunger = " + str(t.p3_hunger) + "\n")
				
				f.write("food = " + str(t.food) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
	else:
		print("You do not have enough food! Purchase more in the shop.")
	f.close()
	
def give_water():
	import t_savefile
	f = open('t_savefile.py', 'a')
	if t.water > 9:	
		option = input("Whick Tagsugotchi would you like to give food to? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			if t.pet_1 != "":
				t.p1_thirst = t.p1_thirst + 15
				t.water = t.water - 10
				print("You gave water to " + str(t.pet_1) + "!")
				
				f.write("p1_thirst = " + str(t.p1_thirst) + "\n")
				
				f.write("water = " + str(t.water) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 2:
			if t.pet_2 != "":
				t.p2_thirst = t.p2_thirst + 15
				t.water = t.water - 10
				print("You gave water to  " + str(t.pet_2) + "!")
				
				f.write("p2_thirst = " + str(t.p2_thirst) + "\n")
				
				f.write("water = " + str(t.water) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
		if option == 3:
			if t.pet_3 != "":
				t.p3_thirst = t.p3_thirst + 15
				t.water = t.water - 10
				print("You gave water to " + str(t.pet_3) + "!")
				
				f.write("p3_thirst = " + str(t.p3_thirst) + "\n")
				
				f.write("water = " + str(t.water) + "\n")
			else:
				print("Please select one of your Tagsugotchi!")
	else:
		print("You do not have enough water! Purchase more in the shop.")
	f.close()

