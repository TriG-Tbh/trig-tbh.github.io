from sense_hat import *
sense = SenseHat()
from random import randint

sense.clear()

def wait_for_move():
	while True:
		e = sense.stick.wait_for_event()
		if e.action != ACTION_RELEASED:
			return e

R = [255, 0, 0]
Y = [255, 255, 0]
G = [0, 255, 0]
W = [255, 255, 255]
B = [0, 0, 255]
Bl = [0, 0, 0]

blank = [
R, R, Bl, Bl, Bl, Bl, R, R, 
R, R, Bl, Bl, Bl, Bl, R, R, 
Bl, Bl, Bl, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, Bl, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, Bl, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, Bl, Bl, Bl, Bl, Bl, Bl, 
R, R, Bl, Bl, Bl, Bl, R, R, 
R, R, Bl, Bl, Bl, Bl, R, R]

start = [
R, R, Bl, Bl, Bl, Bl, R, R, 
R, R, R, R, R, R, R, R, 
Bl, Bl, R, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, R, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, R, Bl, Bl, Bl, Bl, Bl, 
Bl, Bl, R, Bl, Bl, Bl, Bl, Bl, 
R, R, R, R, R, R, R, R, 
R, R, Bl, Bl, Bl, Bl, R, R]

sense.set_pixels(start)

def mapsave(savex, savey):
	current_save = sense.get_pixels()
	return(current_save)

mapx = 0
mapy = 0

mapsave(mapx, mapy)



x = 3
y = 4

sense.set_pixel(x, y, B)
sense.set_pixel(1, 1, R)
current = sense.get_pixel(1, 1)
print(current)

while True:
	e = ""
	e = wait_for_move()
	
	sense.set_pixel(x, y, Bl)
		
	if e.direction == DIRECTION_UP:
		if y > 0:
			y = y - 1
			current = sense.get_pixel(x, y)
			if current == [248, 0, 0]:
				y = y + 1
		else:
			y = 7
			mapy = mapy + 1
			sense.set_pixels(blank)
	elif e.direction == DIRECTION_DOWN:
		if y < 7:
			y = y + 1
			current = sense.get_pixel(x, y)
			if current == [248, 0, 0]:
				y = y - 1
		else:
			y = 0
			mapy = mapy - 1
			sense.set_pixels(blank)	
	elif e.direction == DIRECTION_LEFT: 
		if x > 0:
			x = x - 1
			current = sense.get_pixel(x, y)
			if current == [248, 0, 0]:
				x = x + 1
		else:
			x = 7
			mapx = mapx - 1
			sense.set_pixels(blank)
	elif e.direction == DIRECTION_RIGHT:
		if x < 7:
			x = x + 1
			current = sense.get_pixel(x, y)
			if current == [248, 0, 0]:
				x = x - 1
		else:
			x = 0
			mapx = mapx + 1
			sense.set_pixels(blank)
	print(mapx, mapy)
	sense.set_pixel(x, y, B)
	e = ""

