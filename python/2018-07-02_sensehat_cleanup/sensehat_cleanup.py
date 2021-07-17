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
