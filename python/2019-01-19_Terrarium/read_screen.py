from sense_hat import *
from time import sleep
from random import randint

sense = SenseHat()
sense.clear()

R = [randint(0, 255), randint(0, 255), randint(0, 255)]
W = [255, 255, 255]	
B = [0, 0, 0]

sense.set_pixels([
B, B, B, B, B, B, B, B,
B, W, B, B, B, B, B, B,
B, B, W, B, B, B, B, B,
W, W, W, B, B, B, B, B,
B, B, B, B, B, W, W, W,
B, B, B, B, B, W, B, B,
B, B, B, B, B, B, W, B,
B, B, B, B, B, B, B, B,
])

detectx = 0
detecty = 0
alive_neighbours = 0

sleep(0.5)

while True:
	deadx_list = []
	deady_list = []
	alivex_list = []
	alivey_list = []
	for i in range(1, 9):
		for i in range(1, 9):
			R = [randint(0, 255), randint(0, 255), randint(0, 255)]	
			try:
				current = sense.get_pixel(detectx - 1, detecty + 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx, detecty + 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx + 1, detecty + 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx - 1, detecty)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx + 1, detecty)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx - 1, detecty - 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx, detecty - 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				
				pass
			try:
				current = sense.get_pixel(detectx + 1, detecty - 1)
				if current != B:
					alive_neighbours = alive_neighbours + 1
			except:
				pass
			current = sense.get_pixel(detectx, detecty)
#			raw_input()
			if alive_neighbours < 2 or alive_neighbours > 3:
				deadx_list.append(detectx)
				deady_list.append(detecty)
			if (alive_neighbours == 2 or alive_neighbours == 3) and current != B:
				alivex_list.append(detectx)
				alivey_list.append(detecty)
			if alive_neighbours == 3 and current == B:
				alivex_list.append(detectx)
				alivey_list.append(detecty)
			detectx = detectx + 1
			alive_neighbours = 0
		detectx = 0
		detecty = detecty + 1
	detectx = 0
	detecty = 0
	if len(deadx_list) > 0:
		for i in range(1, len(deadx_list) + 1):
			sense.set_pixel(deadx_list[0], deady_list[0], B)
			del deadx_list[0]
			del deady_list[0]
	if len(alivex_list) > 0:
		for i in range(1, len(alivex_list) + 1):
			sense.set_pixel(alivex_list[0], alivey_list[0], W)
			del alivex_list[0]
			del alivey_list[0]
	R = [randint(0, 255), randint(0, 255), randint(0, 255)]
	sleep(0.5)
