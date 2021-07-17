from sense_hat import *
from time import sleep
from random import randint
from threading import Thread

mythic = [255, 0, 0]
legendary = [255, 255, 0]
epic = [128, 0, 128]
rare = [0, 0, 255]
uncommon = [0, 255, 0]
common = [128, 128, 128]
white = [255, 255, 255]

mythic_value = 6
legendary_value = 5
epic_value = 4
rare_value = 3
uncommon_value = 2
common_value = 1

sense = SenseHat()

tokens = 10
action = "y"
print("You have 10 tokens.")
sleep(1)
while action == "y":
	action = raw_input("Would you like to try your luck at the slot machine? y/n ")
	action.lower
	if action == "y":
		
		print("Removing 4 tokens...")
		sleep(3)
		tokens = tokens - 4
		if tokens < 0:
			print("You have no more tokens! You can\'t play this anymore.")
			sleep(3)
			break

		total = 0
		
		slot_list = []
		
		def slot(x, y):	
			slot_list = []
			for i in range(1, randint(15, 30)):
				selection = randint(1, 6)
				if selection == 1:
					slot_list.append(common)
				if selection == 2:
					slot_list.append(uncommon)
				if selection == 3:
					slot_list.append(rare)
				if selection == 4:
					slot_list.append(epic)
				if selection == 5:
					slot_list.append(legendary)
				if selection == 6:
					slot_list.append(mythic)

			place1 = 0
			
			for i in range(5, randint(10, len(slot_list))):
				sense.set_pixel(x, y, slot_list[place1])
				sleep(0.1)
				place1 = place1 + 1
				
		def celebrate_1_base():
			sense.set_pixel(1, 4, white)
			sleep(0.25)
			sense.set_pixel(0, 4, white)
			sleep(0.25)

		def celebrate_2_base():
			sense.set_pixel(6, 4, white)
			sleep(0.25)
			sense.set_pixel(7, 4, white)
			sleep(0.25)
			
		celebrate_1 = Thread(target = celebrate_1_base)
		celebrate_2 = Thread(target = celebrate_2_base)
		
		slot(2, 4)
		slot(3, 4)
		slot(4, 4)
		slot(5, 4)
			
		sleep(0.25)

		celebrate_1.start()
		celebrate_2.start()

		position_1 = sense.get_pixel(2, 4)
		if position_1 == [248, 0, 0]:
			total = total + mythic_value
		if position_1 == [248, 252, 0]:
			total = total + legendary_value
		if position_1 == [128, 0, 128]:
			total = total + epic_value
		if position_1 == [0, 0, 248]:
			total = total + rare_value
		if position_1 == [0, 252, 0]:
			total = total + uncommon_value
		if position_1 == [128, 128, 128]:
			total = total + common_value
			
		position_1 = sense.get_pixel(3, 4)
		if position_1 == [248, 0, 0]:
			total = total + mythic_value
		if position_1 == [248, 252, 0]:
			total = total + legendary_value
		if position_1 == [128, 0, 128]:
			total = total + epic_value
		if position_1 == [0, 0, 248]:
			total = total + rare_value
		if position_1 == [0, 252, 0]:
			total = total + uncommon_value
		if position_1 == [128, 128, 128]:
			total = total + common_value
			
		position_1 = sense.get_pixel(4, 4)
		if position_1 == [248, 0, 0]:
			total = total + mythic_value
		if position_1 == [248, 252, 0]:
			total = total + legendary_value
		if position_1 == [128, 0, 128]:
			total = total + epic_value
		if position_1 == [0, 0, 248]:
			total = total + rare_value
		if position_1 == [0, 252, 0]:
			total = total + uncommon_value
		if position_1 == [128, 128, 128]:
			total = total + common_value
			
		position_1 = sense.get_pixel(5, 4)
		if position_1 == [248, 0, 0]:
			total = total + mythic_value
		if position_1 == [248, 252, 0]:
			total = total + legendary_value
		if position_1 == [128, 0, 128]:
			total = total + epic_value
		if position_1 == [0, 0, 248]:
			total = total + rare_value
		if position_1 == [0, 252, 0]:
			total = total + uncommon_value
		if position_1 == [128, 128, 128]:
			total = total + common_value

		
		total = (int(total) / 4)

		
		
		print("Amazing! You scored " + str(total) + " tokens!")
		tokens = tokens + total
		print("You now have " + str(tokens) + " tokens.")
		sleep(1)
		
print("Goodbye! Come back soon!")
sleep(1)
sense.clear()
