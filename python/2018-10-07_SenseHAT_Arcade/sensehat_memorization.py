from sense_hat import *
from time import sleep
from random import *
sense = SenseHat()
sense.clear()

m = ""

def memorization():
	
	def wait_for_move2():
		while True:
			m = sense.stick.wait_for_event()
			if m.action != ACTION_RELEASED:
				return m
				
	x = 0
	y = 0

	R = [255, 0, 0]
	G = [0, 255, 0]
	B = [0, 0, 255]
	colors = [R, G, B]
	random_color_picker = randint(0, 2)

	random_color = colors[random_color_picker]

	# Y = [255, 255, 0] (saved for later)
	W = [255, 255, 255]
	Bl = [0, 0, 0]

	color_r = [
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R,
	R, R, R, R, R, R, R, R]

	color_g = [
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G,
	G, G, G, G, G, G, G, G]

	color_b = [
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B,
	B, B, B, B, B, B, B, B]

	sense.clear()


	selection = randint(1, 3)

	if selection == 1:
		sense.set_pixels(color_r)
		color1 = [248, 0, 0]
	elif selection == 2:
		sense.set_pixels(color_g)
		color1 = [0, 252, 0]
	elif selection == 3:
		sense.set_pixels(color_b)
		color1 = [0, 0, 248]
	sleep(0.5)
	sense.clear()
	sleep(0.1)
	selection = randint(1, 3)

	if selection == 1:
		sense.set_pixels(color_r)
		color2 = [248, 0, 0]
	elif selection == 2:
		sense.set_pixels(color_g)
		color2 = [0, 252, 0]
	elif selection == 3:
		sense.set_pixels(color_b)
		color2 = [0, 0, 248]
	sleep(0.5)
	sense.clear()
	sleep(0.1)
	selection = randint(1, 3)

	if selection == 1:
		sense.set_pixels(color_r)
		color3 = [248, 0, 0]
	elif selection == 2:
		sense.set_pixels(color_g)
		color3 = [0, 252, 0]
	elif selection == 3:
		sense.set_pixels(color_b)
		color3 = [0, 0, 248]
	sleep(0.5)
	sense.clear()
	sleep(0.1)
	selection = randint(1, 3)

	if selection == 1:
		sense.set_pixels(color_r)
		color4 = [248, 0, 0]
	elif selection == 2:
		sense.set_pixels(color_g)
		color4 = [0, 252, 0]
	elif selection == 3:
		sense.set_pixels(color_b)
		color4 = [0, 0, 248]
	sleep(0.5)
	sense.clear()
	sleep(0.1)
	selection = randint(1, 3)
	if selection == 1:
		sense.set_pixels(color_r)
		color5 = [248, 0, 0]
	elif selection == 2:
		sense.set_pixels(color_g)
		color5 = [0, 252, 0]
	elif selection == 3:
		sense.set_pixels(color_b)
		color5 = [0, 0, 248]
	sleep(0.5)
	sense.clear()
	sleep(0.1)

	correct_row = randint(1, 4)
	if correct_row == 1:
		sense.set_pixel(3, 0, color1)
		sense.set_pixel(4, 0, color2)
		sense.set_pixel(5, 0, color3)
		sense.set_pixel(6, 0, color4)
		sense.set_pixel(7, 0, color5)
	else:
		random_color = colors[randint(0, 2)]
		sense.set_pixel(3, 0, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(4, 0, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(5, 0, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(6, 0, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(7, 0, random_color)
		
	if correct_row == 2:
		sense.set_pixel(3, 2, color1)
		sense.set_pixel(4, 2, color2)
		sense.set_pixel(5, 2, color3)
		sense.set_pixel(6, 2, color4)
		sense.set_pixel(7, 2, color5)
	else:
		random_color = colors[randint(0, 2)]
		sense.set_pixel(3, 2, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(4, 2, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(5, 2, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(6, 2, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(7, 2, random_color)
	if correct_row == 3:
		sense.set_pixel(3, 4, color1)
		sense.set_pixel(4, 4, color2)
		sense.set_pixel(5, 4, color3)
		sense.set_pixel(6, 4, color4)
		sense.set_pixel(7, 4, color5)
	else:
		random_color = colors[randint(0, 2)]
		sense.set_pixel(3, 4, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(4, 4, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(5, 4, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(6, 4, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(7, 4, random_color)
	if correct_row == 4:
		sense.set_pixel(3, 6, color1)
		sense.set_pixel(4, 6, color2)
		sense.set_pixel(5, 6, color3)
		sense.set_pixel(6, 6, color4)
		sense.set_pixel(7, 6, color5)
	else:
		random_color = colors[randint(0, 2)]
		sense.set_pixel(3, 6, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(4, 6, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(5, 6, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(6, 6, random_color)
		random_color = colors[randint(0, 2)]
		sense.set_pixel(7, 6, random_color)
		
	sense.set_pixel(x, y, W)
		
	
	while True:
		m = ""
		m = wait_for_move2()
		
		if m.direction == DIRECTION_MIDDLE:
			x1 = sense.get_pixel(3, y)
			x2 = sense.get_pixel(4, y)
			x3 = sense.get_pixel(5, y)
			x4 = sense.get_pixel(6, y)
			x5 = sense.get_pixel(7, y)
			if x1 == color1 and x2 == color2 and x3 == color3 and x4 == color4 and x5 == color5:
				sense.set_pixel(x, y, G)
				sleep(1)
				sense.clear()
				return True
			else:
				sense.set_pixel(x, y, R)
				sleep(1)
				sense.clear()
				return False

			sleep(1)
			sense.clear()
			break
		
		sense.set_pixel(x, y, Bl)
		
		if m.direction == DIRECTION_UP and y > 0:
			y = y - 2
		elif m.direction == DIRECTION_DOWN and y < 6:
			y = y + 2
			
		sense.set_pixel(x, y, W)
		m = ""
#memorization()
