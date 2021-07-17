from sense_hat import *
from time import sleep
from random import randint
from threading import Thread

sense = SenseHat()
sense.clear()

P = [255, 20, 147]
B = [0, 0, 0]

def attack_2_base():
	sense.set_pixel(5, 5, P)
