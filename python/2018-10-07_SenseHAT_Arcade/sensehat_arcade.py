from sense_hat import *
from time import sleep
from random import *

from sensehat_goldhunt import goldhunt
from sensehat_memorization import memorization
#from sensehat_memorization import *



#import os


sense = SenseHat()
sense.clear()

go = ""

def arcade():
	game = randint(1, 2)
	if game == 1:
		go = goldhunt()
		if go == True:
			arcade()
	elif game == 2:
		go = memorization()
		if go == True:
			arcade()
	
arcade()
