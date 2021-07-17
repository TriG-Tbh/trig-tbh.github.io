import t_savefile
t = t_savefile
from time import sleep
from threading import Thread
from time import sleep
def p2_lifelike_base():
	while True:
		import t_savefile
		if t.pet_2 != "" and t.p2_current_action == "Idle":
			t.p2_hunger = t.p2_hunger - 5
			t.p2_thirst = t.p2_thirst - 5
			t.p2_sanitation = t.p2_sanitation - 5
			t.p2_happiness = t.p2_happiness - 3
			f = open("t_savefile.py", "a")
			f.write("t.p2_hunger = p2_hunger - 5\n"
			"p2_thirst = p2_thirst - 5\n"
			"p2_sanitation = p2_sanitation - 5\n"
			"p2_happiness = p2_happiness - 3\n")
			if t.p2_hunger < 51:
				print("You need to give " + t.pet_2 + " food!")
			if t.p2_thirst < 51:
				print("You need to give " + t.pet_2 + " water!")
			if t.p2_sanitation < 51:
				print("You need to clean " + t.pet_2 + "!")
			sleep(60 * 60)

def p2_lifelike():
	p2_life = Thread(target = p2_lifelike_base)
	p2_life.start()
	
def p2_neglet_base():
	while True:
		import t_savefile
		if t.pet_2 != "":
			p2_average = (t.p2_sanitation + t.p2_hunger + t.p2_thirst + t.p2_happiness) / 4
			if p2_average < 25:
				print(t.pet_2 + " felt neglected and ran away!")
				sleep(1)
				print("You lost your Tagsugotchi!")
				f = open("t_savefile.py", "a")
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
		sleep(1)

def p2_neglect():
	p2_neglection = Thread(target = p2_neglet_base)
	p2_neglection.start()

p2_lifelike()
p2_neglect()
