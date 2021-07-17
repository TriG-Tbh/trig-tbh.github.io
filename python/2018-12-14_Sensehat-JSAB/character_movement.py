from sense_hat import *
from time import sleep
from random import randint
from threading import Thread

sense = SenseHat()
sense.clear()

B = [0, 0, 0]
Y = [255, 255, 0]
Bl = [0, 0, 255]
R = [255, 0, 0]

P = [255, 20, 147]

global x, y

x = 3
y = 7

sense.set_pixel(x, y, Bl)



def wait_for_move():
	while True:
		e = sense.stick.wait_for_event()
		if e.action != ACTION_RELEASED:
			return e
			
def move(x, y):
	while True:
		e = wait_for_move()
		sense.set_pixel(x, y, B)
		if e.direction == DIRECTION_UP and y > 0:
			y = y - 1
		elif e.direction == DIRECTION_DOWN and y < 7:
			y = y + 1
		elif e.direction == DIRECTION_LEFT and x > 0:
			x = x - 1
		elif e.direction == DIRECTION_RIGHT and x < 7:
			x = x + 1
		print(x, y)
		sense.set_pixel(x, y, Bl)
		e = ""
	
def hit_detection():
	while True:
		
		current = sense.get_pixel(x, y)
		print(x, y)
		print current
		if current == [248, 20, 144]:
			sense.set_pixel(x, y, B)
			sleep(0.1)
			sense.set_pixel(x, y, Bl)
			sleep(0.1)
			sense.set_pixel(x, y, B)
			sleep(0.1)
			sense.set_pixel(x, y, Bl)
		sleep(0.1)
check_for_hit = Thread(target = hit_detection)
check_for_hit.start()




import attack1
attack1.first_attack.start()

while True:
	move_character = Thread(target = move(x, y))
	move_character.start()

move = Thread(target = movement)
move.start()
sense.clear()
import attack1
