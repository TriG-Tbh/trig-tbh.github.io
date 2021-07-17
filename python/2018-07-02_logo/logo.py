from sense_hat import SenseHat
from time import sleep
from random import *

sense = SenseHat()
sense = SenseHat()

X = [0, 0, 0]  # Red
O = [0, 0, 0]  # White

clean_up = [
O, O, O, X, X, O, O, O,
O, O, X, O, O, X, O, O,
O, O, O, O, O, X, O, O,
O, O, O, O, X, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, X, O, O, O, O,
O, O, O, O, O, O, O, O,
O, O, O, X, O, O, O, O
]

sense.set_pixels(clean_up)


for x in range(0, 4):
	for y in range(0, 4):
		sense.set_pixel(int(x), int(y), 255, 0, 0)
		sleep(0.1)
		
for x in range(4, 5):
	for y in range(0, 4):
		sense.set_pixel(int(x), int(y), 255, 100, 0)
		sleep(0.1)
		
for x in range(5, 8):
	for y in range(3, 4):
		sense.set_pixel(int(x), int(y), 255, 100, 0)
		sleep(0.1)


for x in range(0, 4):
	for y in range(4, 5):
		sense.set_pixel(int(x), int(y), 255, 100, 0)
		sleep(0.1)

for x in range(3, 4):
	for y in range(5, 8):
		sense.set_pixel(int(x), int(y), 255, 100, 0)
		sleep(0.1)
		

for x in range(4, 8):
	for y in range(4, 8):
		sense.set_pixel(int(x), int(y), 255, 255, 0)
		sleep(0.1)

