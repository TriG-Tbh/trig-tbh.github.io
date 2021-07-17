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



def clean():
	from t_savefile import cleaning_supplies
	t = t_savefile
	print t.cleaning_supplies
	if t.cleaning_supplies > 9:	
		option = input("Whick Tagsugotchi would you like to clean? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			t.p1_sanitation = t.p1_sanitation + 15
			t.cleaning_supplies = t.cleaning_supplies - 10
			print("You cleaned " + t.pet_1 + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p1_sanitation = \"" + int(t.p1_sanitation) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("cleaning_supplies = \"" + int(t.cleaning_supplies) + "\"\n")
		if option == 2:
			t.p2_sanitation = t.p2_sanitation + 15
			cleaning_supplies = cleaning_supplies - 10
			print("You cleaned " + t.pet_2 + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p2_sanitation = \"" + int(t.p2_sanitation) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("cleaning_supplies = \"" + int(t.cleaning_supplies) + "\"\n")
		if option == 3:
			t.p3_sanitation = t.p3_sanitation + 15
			t.cleaning_supplies = t.cleaning_supplies - 10
			print("You cleaned " + t.pet_3 + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p3_sanitation = \"" + int(t.p3_sanitation) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("cleaning_supplies = \"" + int(t.cleaning_supplies) + "\"\n")
	else:
		print("You do not have enough cleaning supplies! Purchase more in the shop.")

def feed():
	import t_savefile
	if t.food > 9:	
		option = input("Whick Tagsugotchi would you like to give food to? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			t.p1_hunger = t.p1_hunger + 15
			t.food = t.food - 10
			print("You gave food to " + str(t.pet_1) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p1_hunger = \"" + int(t.p1_hunger) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("food = \"" + int(t.food) + "\"\n")
		if option == 2:
			t.p2_hunger = t.p2_hunger + 15
			t.food = t.food - 10
			print("You gave food to " + str(t.pet_2) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p2_hunger = \"" + int(t.p2_hunger) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("food = \"" + int(t.food) + "\"\n")
		if option == 3:
			t.p3_hunger = t.p3_hunger + 15
			t.food = t.food - 10
			print("You gave food to " + str(t.pet_3) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p3_hunger = \"" + int(t.p3_hunger) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("food = \"" + int(t.food) + "\"\n")
	else:
		print("You do not have enough food! Purchase more in the shop.")

def give_water():
	import t_savefile
	if t.water > 9:	
		option = input("Whick Tagsugotchi would you like to give food to? \n"
		"1) " + t.pet_1 + "\n"
		"2) " + t.pet_2 + "\n"
		"3) " + t.pet_3 + "\n"
		"Please select one of your Tagsugotchi (1-3): ")
		if option == 1:
			t.p1_thirst = t.p1_thirst + 15
			t.water = t.water - 10
			print("You gave water to " + str(t.pet_1) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p1_thirst = \"" + int(t.p1_thirst) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("water = \"" + int(t.water) + "\"\n")
		if option == 2:
			t.p2_thirst = t.p2_thirst + 15
			t.water = t.water - 10
			print("You gave water to  " + str(t.pet_2) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p2_thirst = \"" + int(t.p2_thirst) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("water = \"" + int(t.water) + "\"\n")
		if option == 3:
			t.p3_thirst = t.p3_thirst + 15
			t.water = t.water - 10
			print("You gave water to " + str(t.pet_3) + "!")
			with open('t_savefile.py', 'a') as f:
				f.write("p3_thirst = \"" + int(t.p3_thirst) + "\"\n")
			with open('t_savefile.py', 'a') as f:
				f.write("water = \"" + int(t.water) + "\"\n")
	else:
		print("You do not have enough water! Purchase more in the shop.")

