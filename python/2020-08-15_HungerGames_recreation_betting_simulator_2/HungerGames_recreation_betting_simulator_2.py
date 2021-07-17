from __future__ import print_function
from random import randint
from time import sleep
import random
import pdb

standby_list = []
trib_alliance_list = []
alliance_done_list = []
trib_done_list = []
trib_dead = []
trib1_list = []
trib2_list = []
trib3_list = []
dead_copy = []

trib_action = randint(1, 5)

day_of_battle = 1
trib_selected_1 = ""
trib_selected_2 = ""
trib_selected_3 = ""
number_of_actions = ""
trib_done_with_action = 0 
selecting_redo = 0
first_selection = 0
alliance_check = 0
alliance_in_play = 0
team_override = 0
event_list_len = 0
trib_1_copy = ""
trib_2_copy = ""
trib_3_copy = ""
checking_for_standoff = 0

list_num = 0
list_num2 = 0

trib_name = ""
trib_counter = 1
trib_counter = str(trib_counter)

num_of_tribs = input("Number of tributes: ")
for i in range(1, int(num_of_tribs) + 1):
	trib_counter = str(trib_counter)
	trib_name = input("Name of tribute " + str(trib_counter) + ": ")
	standby_list.append(trib_name)
	trib_name = ""
	trib_counter = int(trib_counter)
	trib_counter = int(trib_counter) + 1

while (len(standby_list) + len(trib_alliance_list) + len(alliance_done_list) + len(trib_done_list)) > 1:
	day_of_battle = str(day_of_battle)
	print("DAY " + str(day_of_battle))
	sleep(1)
	print("FIGHT")
	sleep(1)
	day_of_battle = int(day_of_battle)
	day_of_battle = day_of_battle + 1
	
	number_of_actions = randint(1, (len(standby_list) + len(trib_alliance_list)))
	print(number_of_actions)
	for i in range(number_of_actions):
		if team_override == 1:
			alliance_in_play = 1
		print(standby_list)
		if "[]" in standby_list:
			while "[]" in standby_list:
				standby_list.remove("[]")
		selecting_redo = 1
		while selecting_redo == 1:
			first_selection = randint(1, 3)
			print(first_selection)
			if first_selection == 1:
				if len(standby_list) > len(trib_alliance_list):
					trib_selected_1 = random.choice(standby_list)
					
					selecting_redo = 0
				else:
					
					trib_selected_1 = random.choice(trib_alliance_list)
					selecting_redo = 0
				
			else:
				if first_selection == 2:
					if len(trib_alliance_list) > len(standby_list):
						
						trib_selected_1 = random.choice(trib_alliance_list)
						
						selecting_redo = 0
					else:
						
						trib_selected_1 = random.choice(standby_list)
						selecting_redo = 0
		
		trib_1_copy = trib_selected_1
				
		#pdb.set_trace()
		selecting_redo = 1
		if len(standby_list) > len(trib_alliance_list):
			trib_selected_2 = random.choice(standby_list)
			if trib_selected_2 == trib_selected_1:
				while trib_selected_1 == trib_selected_2:
					trib_selected_2 = random.choice(standby_list)
			print("standby")
			
		else:
			if len(trib_alliance_list) > len(alliance_done_list):
				if trib_selected_1 not in trib_alliance_list:
					trib_selected_2 = random.choice(trib_alliance_list)
					if trib_selected_2 == trib_selected_1:
						while trib_selected_1 == trib_selected_2:
							trib_selected_2 = random.choice(trib_alliance_list)
				print("alliance")

			else:				
				if len(alliance_done_list) > len(trib_done_list):	
					if trib_selected_1 not in alliance_done_list:
						trib_selected_2 = random.choice(alliance_done_list)
						if trib_selected_2 == trib_selected_1:
							while trib_selected_1 == trib_selected_2:
								trib_selected_2 = random.choice(alliance_done_list)
					print("done")
				
				else:
					if len(trib_done_list) > 2:
						trib_selected_2 = random.choice(trib_done_list)
						if trib_selected_2 == trib_selected_1:
							while trib_selected_1 == trib_selected_2:
								trib_selected_2 = random.choice(trib_done_list)
						print("trib_done")
					else:
						trib_selected_2 = random.choice(standby_list)
						if trib_selected_2 == trib_selected_1:
							while trib_selected_1 == trib_selected_2:
								trib_selected_2 = random.choice(standby_list)
						
		
		trib_2_copy = trib_selected_2
		#print("trib2 complete")			
		selecting_redo = 1
	
		if len(standby_list) > len(trib_alliance_list):
			trib_selected_3 = random.choice(standby_list)
			if trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
				while trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
					trib_selected_3 = random.choice(standby_list)
				

			selecting_redo = 0
		else:		
			if len(trib_alliance_list) > len(alliance_done_list):
				if trib_selected_1 not in trib_alliance_list:
					trib_selected_3 = random.choice(trib_alliance_list)
					if trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
						while trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
							trib_selected_3 = random.choice(trib_alliance_list)
				
						
				
			else:
				if len(alliance_done_list) > len(trib_done_list):	
					if trib_selected_1 not in alliance_done_list:
						trib_selected_3 = random.choice(alliance_done_list)
						if trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
							while trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
							       trib_selected_3 = random.choice(alliance_done_list)
				
				else:
					if len(trib_done_list) > 2:
						trib_selected_3 = random.choice(trib_done_list)
						if trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
							while trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
								trib_selected_3 = random.choice(trib_done_list)
					else:
						trib_selected_3 = random.choice(standby_list)
						if trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
							while trib_selected_3 == trib_selected_2 or trib_selected_3 == trib_selected_1:
								trib_selected_3 = random.choice(standby_list)
		
		trib_3_copy = trib_selected_3
		#print("trib3 complete")
		print(trib_selected_1)
		print(trib_selected_2)
		print(trib_selected_3)
		trib_action = randint(1, 5)
		#pdb.set_trace()
		trib1_list.append(trib_selected_1)
		trib2_list.append(trib_selected_2)
		trib3_list.append(trib_selected_3)
		alliance_check = 1
		alliance_check = 1
		while alliance_check == 1:
			trib_action = randint(1, 5)
			checking_for_standoff = 1
			while checking_for_standoff == 1:
				if trib_action == 3:
					if (len(standby_list) + len(trib_done_list)) == 2:
						trib_action = randint(1, 5)
					else:
						checking_for_standoff = 0
				else:
					checking_for_standoff = 0
			#print(trib_action)
			if trib_action == 1:
				if trib_selected_1 in trib_alliance_list:
					if len(standby_list) > len(trib_done_list):
						trib_selected_2 = random.choice(standby_list)
						if trib_selected_2 == trib_selected_1:
							while trib_selected_1 == trib_selected_2:
							       trib_selected_2 = random.choice(standby_list)
					else:
						if len(trib_done_list) > 2:
							trib_selected_2 = random.choice(trib_done_list)
							if trib_selected_2 == trib_selected_1:
								while trib_selected_1 == trib_selected_2:
									trib_selected_2 = random.choice(trib_done_list)
						else:
							trib_selected_2 = random.choice(standby_list)
							if trib_selected_2 == trib_selected_1:
								while trib_selected_1 == trib_selected_2:
									trib_selected_2 = random.choice(standby_list)
			
			
		
				trib_selected_1 = str(trib_selected_1)
				trib_selected_2 = str(trib_selected_2)
				print(str(trib_selected_1) + " killed " + str(trib_selected_2))
				trib_selected_1 = trib_1_copy
				trib_selected_2 = trib_2_copy
				if trib_selected_2 in standby_list:
					standby_list.remove(trib_selected_2)
				if trib_selected_2 in trib_alliance_list:
					trib_alliance_list.remove(trib_selected_2)
				if trib_selected_2 in alliance_done_list:
					alliance_done_list.remove(trib_selected_2)
				if trib_selected_2 in trib_done_list:
					trib_done_list.remove(trib_selected_2)
				if trib_selected_2 not in trib_dead:
					trib_dead.append(trib_selected_2)
				if trib_selected_1 in standby_list:
					standby_list.remove(trib_selected_1)
					trib_done_list.append(trib_selected_1)
					trib_done_list += (trib_selected_1)
				if trib_selected_1 in trib_alliance_list:
					trib_alliance_list.remove(trib_selected_1)
					alliance_done_list.append(trib_selected_1)
					alliance_done_list += (trib_selected_1)
				if trib_selected_1 in standby_list and not trib_done_list:
					standby_list.remove(trib_selected_1)
					trib_done_list.append(trib_selected_1)
					trib_done_list += (trib_selected_1)
				if trib_selected_1 in trib_alliance_list and not alliance_done_list:
					trib_alliance_list.remove(trib_selected_1)
					alliance_done_list.append(trib_selected_1)
					alliance_done_list += (trib_selected_1)
				alliance_check = 0
			
			elif trib_action == 2:
				trib_selected_1 = str(trib_selected_1)
				print(str(trib_selected_1) + " made a shack")
				trib_selected_1 = trib_1_copy
				if trib_selected_1 in standby_list:
					standby_list.remove(trib_selected_1)
					trib_done_list.append(trib_selected_1)
					trib_done_list += (trib_selected_1)
				if trib_selected_1 in trib_alliance_list:
					trib_alliance_list.remove(trib_selected_1)
					alliance_done_list.append(trib_selected_1)
					alliance_done_list += (trib_selected_1)
				if trib_selected_1 in standby_list and not trib_done_list:
					standby_list.remove(trib_selected_1)
					trib_done_list.append(trib_selected_1)
					trib_done_list += (trib_selected_1)
				if trib_selected_1 in trib_alliance_list and not alliance_done_list:
					trib_alliance_list.remove(trib_selected_1)
					alliance_done_list.append(trib_selected_1)
					alliance_done_list += (trib_selected_1)
				alliance_check = 0
				
			elif trib_action == 3:
				if alliance_in_play == 0:
					if (trib_selected_1 not in trib_alliance_list or trib_selected_1 not in alliance_done_list) and (trib_selected_2 not in trib_alliance_list or trib_selected_2 not in alliance_done_list) and (trib_selected_3 not in trib_alliance_list or trib_selected_3 not in alliance_done_list):
						trib_selected_1 = str(trib_selected_1)
						trib_selected_2 = str(trib_selected_2)
						trib_selected_3 = str(trib_selected_3)
						print(str(trib_selected_1) + " formed an alliance with " + str(trib_selected_2) + " and " + str(trib_selected_3))
						trib_selected_1 = trib_1_copy
						trib_selected_2 = trib_2_copy
						trib_selected_3 = trib_3_copy
						if trib_selected_1 in standby_list:
							standby_list.remove(trib_selected_1)
						trib_alliance_list.append(trib_selected_1)
						trib_alliance_list += (trib_selected_1)
						if trib_selected_1 in alliance_done_list:
							alliance_done_list.remove(trib_selected_1)
						if trib_selected_1 in trib_done_list:
							trib_done_list.remove(trib_selected_1)
						if trib_selected_2 in standby_list:
							standby_list.remove(trib_selected_2)
						trib_alliance_list.append(trib_selected_2)
						trib_alliance_list += (trib_selected_2)
						if trib_selected_2 in alliance_done_list:
							alliance_done_list.remove(trib_selected_2)
						if trib_selected_2 in trib_done_list:
							trib_done_list.remove(trib_selected_2)
						if trib_selected_3 in standby_list:
							standby_list.remove(trib_selected_3)
						trib_alliance_list.append(trib_selected_3)
						trib_alliance_list += (trib_selected_3)
						if trib_selected_3 in alliance_done_list:
							alliance_done_list.remove(trib_selected_3)
						if trib_selected_3 in trib_done_list:
							trib_done_list.remove(trib_selected_3)
						alliance_check = 0
						alliance_in_play = 1
					else:
						alliance_check = 1
				else:
					alliance_check = 1
					
			elif trib_action == 4: 	
				trib_selected_1 = str(trib_selected_1)	
				print(str(trib_selected_1) + " fell into a pit and died")
				trib_selected_1 = trib_1_copy
				if trib_selected_1 in standby_list:
					standby_list.remove(trib_selected_1)
				if trib_selected_1 in trib_alliance_list:
					trib_alliance_list.remove(trib_selected_1)
				if trib_selected_1 in alliance_done_list:
					alliance_done_list.remove(trib_selected_1)
				if trib_selected_1 in trib_done_list:
					trib_done_list.remove(trib_selected_1)
				trib_dead.append(trib_selected_1)
				alliance_check = 0
			
			
		sleep(3)		


		#print(trib_selected_1)
		#print(trib_selected_2)
		#print(trib_selected_3)
						
		if trib_selected_1 in trib_alliance_list:
			alliance_done_list.append(trib_selected_1)
			trib_alliance_list.remove(trib_selected_1)
		else:
			if trib_selected_1 not in trib_dead:
				if trib_selected_1 not in trib_done_list:
					trib_done_list.append(trib_selected_1)
				if trib_selected_1 in standby_list:
					standby_list.remove(trib_selected_1)
		
		trib_selected_1 = ""
		trib_selected_2 = ""
		trib_selected_3 = ""
		
		if (len(trib_alliance_list) + len(alliance_done_list)) != 0:
			alliance_in_play = 1
		else:
			alliance_in_play = 0
			
		if team_override == 1:
			alliance_in_play = 1
		
		trib1_list.clear()
		trib2_list.clear()
		trib3_list.clear()
		if len(standby_list) + len(trib_done_list) == 0 and len(alliance_done_list) + len(trib_done_list) > len(standby_list) + len(trib_done_list):
			print("The alliance disbanded!")
			standby_list += trib_alliance_list.copy()
			standby_list += alliance_done_list.copy()
			trib_alliance_list = []
			alliance_done_list = []
			team_override = 1
		if (len(trib_alliance_list) + len(alliance_done_list)) == 1:
			standby_list += trib_alliance_list.copy()
			standby_list += alliance_done_list.copy()
			trib_alliance_list = []
			alliance_done_list = []
		if len(standby_list) + len(trib_alliance_list) > number_of_actions:
			number_of_actions = 0
		
	
	#print(trib_done_list)
	
	if len(trib_dead) > 0:
		dead_copy = trib_dead
		#trib_dead = str(trib_dead)
		print("The dead tributes are: " + "\n")
		print(", ".join(trib_dead))
		#trib_dead = dead_copy
		trib_dead = []
	if len(trib_done_list) > 0:
		standby_list = trib_done_list.copy()

		trib_done_list = []
	if len(alliance_done_list) > 0:
		trib_alliance_list = alliance_done_list.copy()
		alliance_done_list = []
	if len(standby_list) < 3:
		team_override = 1
	

		
if len(standby_list) > len(trib_done_list):
	print(str(random.choice(standby_list)) + " is the winner!")
else:		
	print(str(random.choice(trib_done_list)) + " is the winner!")
