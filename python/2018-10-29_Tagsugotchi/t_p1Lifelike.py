import t_savefile
t = t_savefile
from time import sleep
from threading import Thread
from time import sleep
def p1_lifelike_base():
	while True:
		import t_savefile
		if t.pet_1 != "" and t.p1_current_action == "Idle":
			t.p1_hunger = t.p1_hunger - 5
			t.p1_thirst = t.p1_thirst - 5
			t.p1_sanitation = t.p1_sanitation - 5
			t.p1_happiness = t.p1_happiness - 3
			f = open("t_savefile.py", "a")
			f.write("t.p1_hunger = p1_hunger - 5\n"
			"p1_thirst = p1_thirst - 5\n"
			"p1_sanitation = p1_sanitation - 5\n"
			"p1_happiness = p1_happiness - 3\n")
			if t.p1_hunger < 51:
				print("You need to give " + t.pet_1 + " food!")
			if t.p1_thirst < 51:
				print("You need to give " + t.pet_1 + " water!")
			if t.p1_sanitation < 51:
				print("You need to clean " + t.pet_1 + "!")
			sleep(60 * 60)

def p1_lifelike():
	p1_life = Thread(target = p1_lifelike_base)
	p1_life.start()
	
def p1_neglet_base():
	while True:
		import t_savefile
		if t.pet_1 != "":
			p1_average = (t.p1_sanitation + t.p1_hunger + t.p1_thirst + t.p1_happiness) / 4
			if p1_average < 25:
				print(t.pet_1 + " felt neglected and ran away!")
				sleep(1)
				print("You lost your Tagsugotchi!")
				f = open("t_savefile.py", "a")
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
		sleep(1)

def p1_neglect():
	p1_neglection = Thread(target = p1_neglet_base)
	p1_neglection.start()

p1_lifelike()
p1_neglect()
