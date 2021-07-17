x1 = ""
x2 = ""
x3 = ""
y1 = ""
y2 = ""
y3 = ""


from sense_hat import *
from time import sleep
from random import *
from threading import Thread

sense = SenseHat()
sense.clear()

def wait_for_move():
	while True:
		e = sense.stick.wait_for_event()
		if e.action != ACTION_RELEASED:
			return e
			
B = [0, 0, 0]
Y = [255, 255, 0]
Bl = [0, 0, 255]
R = [255, 0, 0]

sense.clear()

option = randint(1, 4)
if option == 1:
	x1 = 2
	y1 = 4
	x2 = 3
	y2 = 4
	x3 = 4
	y3 = 4
elif option == 2:
	x1 = 3
	y1 = 4
	x2 = 4
	y2 = 4
	x3 = 5
	y3 = 4
elif option == 3:
	x1 = 4
	y1 = 4
	x2 = 5
	y2 = 4
	x3 = 2
	y3 = 4
elif option == 4:
	x1 = 2
	y1 = 4
	x2 = 3
	y2 = 4
	x3 = 5
	y3 = 4
print option
player_x = 2
player_y = 5
def show_attack():	
	
	for i in range(1, 4):
		sense.set_pixel(x1, y1, Y)
		sense.set_pixel(x2, y2, Y)
		sense.set_pixel(x3, y3, Y)
		sleep(0.2)
		sense.set_pixel(x1, y1, B)
		sense.set_pixel(x2, y2, B)
		sense.set_pixel(x3, y3, B)
		sleep(0.2)
	sense.set_pixel(x1, y1+1, R)
	sense.set_pixel(x2, y2+1, R)
	sense.set_pixel(x3, y3+1, R)
	sleep(1)
	sense.set_pixel(x1, y1, B)
	sense.set_pixel(x2, y2, B)
	sense.set_pixel(x3, y3, B)
sense.set_pixel(player_x, player_y, Bl)
def move():
	for i in range(1, 4):
		e = wait_for_move()
		
		if e.direction == DIRECTION_LEFT:
			if player_x > 2:
				player_x = player_x - 1
		elif e.direction == DIRECTION_RIGHT:
			if player_x < 5:
				player_x = player_x + 1
		sense.set_pixel(player_x, player_y, Bl)
		
move_character = Thread(target = move)
attack = Thread(target = show_attack)

move_character.start()
attack.start()

sense.clear()
