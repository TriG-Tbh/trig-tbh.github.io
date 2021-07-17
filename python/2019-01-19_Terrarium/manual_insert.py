from time import sleep
from sense_hat import SenseHat
import os
sense = SenseHat()
from threading import Thread

action = ""

dropx = 0
dropy = 0

Bl = [0, 0, 255]
B = [0, 0, 0]

sense.set_pixel(dropx, dropy, Bl)


				
def move_base(dropx, dropy):
	def wait_for_move():
		while True:
			f = sense.stick.wait_for_event()
			if f.action != ACTION_RELEASED:
				return f
	while action != "stop":
		e = wait_for_move()
		sense.set_pixel(dropx, dropy, B)
		if e.direction == DIRECTION_UP and y > 0:
			y = y - 1
		elif e.direction == DIRECTION_DOWN and y < 7:
			y = y + 1
		elif e.direction == DIRECTION_LEFT and x > 0:
			x = x - 1
		elif e.direction == DIRECTION_RIGHT and x < 7:
			x = x + 1
		elif e.direction == DIRECTION_MIDDLE:
			current = sense.get_pixel(dropx, dropy)
			#if current == B:
				
		print(x, y)
		sense.set_pixel(x, y, Bl)
		e = ""

def ask_base():
	while True:
		os.system('clear')
		action = raw_input("Say \"stop\" at any time to stop inserting. \n"
		">")
	
def insert():
	move = Thread(target = move_base(0, 0))
	ask = Thread(target = ask_base)
	move.start()
	ask.start()

insert()
