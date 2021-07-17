from sense_hat import *
from time import sleep
from random import randint
from threading import Thread

sense = SenseHat()

sense.clear()
P = [255, 20, 147]
B = [0, 0, 0]

def attack_1_base():
	for i in range(randint(1, 1)):
		random_column = randint(0, 7)
		sense.set_pixel(random_column, 0, P)
		sleep(0.5)
		sense.set_pixel(random_column, 0, B)
		row = 1
		for i in range(1, 8):
			sense.set_pixel(random_column, row, P)
			sleep(0.5)
			sense.set_pixel(random_column, row, B)
			row = row + 1
def attack_1():
	for i in range(1, randint(15, 30)):
		attack_1 = Thread(target = attack_1_base)
		attack_1.start()
		sleep(0.5)
first_attack = Thread(target = attack_1)
