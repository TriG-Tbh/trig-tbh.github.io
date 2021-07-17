import t_savefile
t = t_savefile
from time import sleep
from threading import Thread
from time import sleep
def p3_lifelike_base():
	while True:
		import t_savefile
		if t.pet_3 != "" and t.p3_current_action == "Idle":
			t.p3_hunger = t.p3_hunger - 5
			t.p3_thirst = t.p3_thirst - 5
			t.p3_sanitation = t.p3_sanitation - 5
			t.p3_happiness = t.p3_happiness - 3
			f = open("t_savefile.py", "a")
			f.write("t.p3_hunger = p3_hunger - 5\n"
			"p3_thirst = p3_thirst - 5\n"
			"p3_sanitation = p3_sanitation - 5\n"
			"p3_happiness = p3_happiness - 3\n")
			if t.p3_hunger < 51:
				print("You need to give " + t.pet_3 + " food!")
			if t.p3_thirst < 51:
				print("You need to give " + t.pet_3 + " water!")
			if t.p3_sanitation < 51:
				print("You need to clean " + t.pet_3 + "!")
			sleep(60 * 60)

def p3_lifelike():
	p3_life = Thread(target = p3_lifelike_base)
	p3_life.start()
	
def p3_neglet_base():
	while True:
		import t_savefile
		if t.pet_3 != "":
			p3_average = (t.p3_sanitation + t.p3_hunger + t.p3_thirst + t.p3_happiness) / 4
			if p3_average < 25:
				print(t.pet_3 + " felt neglected and ran away!")
				sleep(1)
				print("You lost your Tagsugotchi!")
				f = open("t_savefile.py", "a")
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
		sleep(1)

def p3_neglect():
	p3_neglection = Thread(target = p3_neglet_base)
	p3_neglection.start()

p3_lifelike()
p3_neglect()
