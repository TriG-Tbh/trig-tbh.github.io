import random
import os


while True:
    os.system("clear")
    doors = [0, 0, 0]
    index = random.randint(0, len(doors) - 1)
    doors[index] = 1
    choiceindex = random.randint(0, len(doors) - 1)
    choice = doors[choiceindex]
    