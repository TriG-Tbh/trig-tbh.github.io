import pynput
from pynput.mouse import Button, Controller
import time
import random

mouse = Controller()

movement = 5

while True:
    mouse.move(random.randint(-movement, movement), 0)
    mouse.move(0, random.randint(-movement, movement))
    time.sleep(0.01)
    click = random.randint(1, 100)
    if click == 1:
        button = random.randint(1, 3)
        if button == 1:
            mouse.click(Button.left)
        elif button == 2:
            mouse.click(Button.right)
        elif button == 3:
            mouse.click(Button.middle)