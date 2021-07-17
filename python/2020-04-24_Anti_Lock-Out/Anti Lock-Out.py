import pynput
from pynput.mouse import Button, Controller
import time
import random

mouse = Controller()

control = 5

while True:
    mouse.move(random.randint(-control, control),
               random.randint(-control, control))
