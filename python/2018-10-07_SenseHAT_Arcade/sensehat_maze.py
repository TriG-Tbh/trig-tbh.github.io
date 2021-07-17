from sense_hat import *
from time import sleep
from random import *
from threading import Thread
import sys

sense = SenseHat()
sense.clear()

plague_do = True

def wait_for_move():
	while True:
		e = sense.stick.wait_for_event()
		if e.action != ACTION_RELEASED:
			return e
			
White = [255, 255, 255]
B = [0, 0, 0]
Y = [255, 255, 0]
G = [0, 255, 0]
Blue = [0, 0, 255]

x = 3
y = 4

play = True

maze_start = [
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, White, White, White, White, White, White,
B, B, White, B, B, B, B, B,
B, B, White, B, B, B, B, B,
B, B, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B]

maze_left = [
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, B, B, B, White, B, B,
B, B, B, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, B, B,
B, B, B, B, Y, White, B, B,
B, B, B, B, B, White, B, B,
White, White, White, White, White, White, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B]
]

maze_up = [
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, B, B, B,
B, B, White, B, B, B, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, B, B, B, White, B, B,
B, B, B, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, Y, White, B, B,
B, B, White, White, White, White, B, B,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B]
]

maze_down = [
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, B, B, B,
B, B, White, B, B, B, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, B, B, B, White, B, B,
B, B, B, B, B, White, B, B,
White, White, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, White, White, White, White, B, B,
B, B, White, B, Y, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B]
]

maze_right = [
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, B, B, B,
B, B, White, B, B, B, B, B,
B, B, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B],
[B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B,
White, White, White, B, B, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
White, White, White, B, B, White, White, White,
B, B, White, B, B, White, B, B,
B, B, White, B, B, White, B, B],
[B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B,
B, B, White, White, White, White, White, White,
B, B, White, Y, B, B, B, B,
B, B, White, B, B, B, B, B,
B, B, White, White, White, White, White, White,
B, B, B, B, B, B, B, B,
B, B, B, B, B, B, B, B]
]

Y = [248, 252, 0]
White = [248, 252, 248]
B = [0, 0, 0]

bh_pos_x = 4
bh_pos_y = 4

def plague():
	for i in range(1, 16):
		if plague_do == True:
			sleep(1)
			Orange = [255, 165, 0]
			bh_pos_x = randint(0, 7)
			bh_pos_y = randint(0, 7)
			sense.set_pixel(bh_pos_x, bh_pos_y, Orange)	
	else:
		sys.exit(0)
	
do_plague = Thread(target = plague)
	

for i in range(1, 2):
	x = 3
	y = 4
	sense.set_pixels(maze_start)
	sense.set_pixel(x, y, Blue)
	while play:
		e = wait_for_move()
		if e.direction != DIRECTION_MIDDLE:
			sense.set_pixel(x, y, B)
		if e.direction == DIRECTION_UP:
			y = y - 1
			if y > -1:
				next_thing = sense.get_pixel(x, y)
				print next_thing
						
				if next_thing != B and next_thing != Y:
					y = y + 1
			else:
				y = 7
				sense.set_pixels(maze_down[randint(0, 4)])
				bh_pos_x = ""
				bh_pos_y = ""
				do_plague.start()
				sense.set_pixel(x, y, Blue)

			current = sense.get_pixel(x, y)
			if current != B: 
				if current != White:
					sense.set_pixel(x, y, G)
					play = False
					print("BOI")
			sense.set_pixel(x, y, Blue)
		elif e.direction == DIRECTION_DOWN:
			y = y + 1
			
			if y < 8:
				next_thing = sense.get_pixel(x, y)
				if next_thing != B and next_thing != Y:
					y = y - 1
			else:
				y = 0
				sense.set_pixels(maze_up[randint(0, 4)])
			current = sense.get_pixel(x, y)
			if current != B: 
				if current != White:
					sense.set_pixel(x, y, G)
					play = False
			sense.set_pixel(x, y, Blue)
		elif e.direction == DIRECTION_LEFT:
			x = x - 1
			if x > 0:
				next_thing = sense.get_pixel(x, y)
			
				if next_thing != B and next_thing != Y:
					x = x + 1
			else:
				x = 7
				sense.set_pixels(maze_right[randint(0, 4)])
			
			current = sense.get_pixel(x, y)
			if current != B:
				if current != White:
					sense.set_pixel(x, y, G)
					play = False
			sense.set_pixel(x, y, Blue)
		elif e.direction == DIRECTION_RIGHT:
			x = x + 1
			if x < 8:
				next_thing = sense.get_pixel(x, y)
			
				if next_thing != B and next_thing != Y:
					x = x - 1
			else:
				x = 0
				sense.set_pixels(maze_left[randint(0, 4)])
			
			current = sense.get_pixel(x, y)
			if current != B: 
				if current != White:
					sense.set_pixel(x, y, G)
					play = False
			sense.set_pixel(x, y, Blue)
	sleep(0.5)
	sense.clear()
	plague_do = False
