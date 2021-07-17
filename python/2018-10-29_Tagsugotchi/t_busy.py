import t_savefile
t = t_savefile
from time import sleep
from random import randint
import datetime
import t_p1_busysave
p1_b = t_p1_busysave
now = datetime.datetime.now()
def p1_busy_base():
	while True:
		import t_savefile
		if now.hour == 20:
			if t.p1_current_action == "Idle":
				#sleep(60 * 60 * (randint(6, 9)))
				p1_b.p1_busy = (60 * 60 * randint(6, 9))
				p1_b.p1_busy = str(p1_b.p1_busy)
				print(t.pet_1 + " fell asleep!")
				p1_b.p1_busy = int(p1_b.p1_busy)
				f = open("t_savefile.py", "a")
				f.write("p1_current_action = \"Sleeping\"")
				f.close()
				f = open("t_p1_busysave.py", "w")
				p1_b.p1_busy = str(p1_b.p1_busy)
				f.write("p1_busy = " + p1_b.p1_busy)
				import t_p1_busysave
				while p1_b.p1_busy != 0:
					sleep(1)
					p1_b.p1_busy = int(p1_b.p1_busy)
					p1_b.p1_busy += int(-1)
					p1_b.p1_busy = str(p1_b.p1_busy)
					f.write("p1_busy = " + p1_b.p1_busy)
				print(t.pet_1 + " woke up!")
		else:
			import t_p1_busysave
			import t_savefile
			f = open("t_p1_busysave.py", "w")
			if t.p1_current_action == "Sleeping":
				while p1_b.p1_busy != 0:
					sleep(1)
					p1_b.p1_busy += int(-1)
					f.write("p1_busy = " + p1_b.p1_busy)
				print(t.pet_1 + " woke up!")
			elif t.p1_current_action == "On A Quest":
				while p1_b.p1_busy != 0:
					sleep(1)
					p1_b.p1_busy += (int(-1))
					f.write("p1_busy = " + p1_b.p1_busy)
				print(t.pet_1 + " finished their quest:")
				sleep(1)
				print("They got...")
				sleep(3)
				t.food = randint(-50, 100)
				t.water = randint(-50, 100)
				t.cleaning_supplies = randint(-50, 100)
				print(t.food + " food...")
				sleep(1)
				print(t.water
p1_busy_base()
