import sys
import time

default = 0.05

def formatstring(character, string):
    return character.color + ": " + string + "\u001b[0m"

def delayprint(string, delay=default):
    for c in string:
        sys.stdout.write(c)
        sys.stdout.flush()
        time.sleep(delay)
    response = input(" ")
    return response

#class Character:
#    def __init__(name, color, )

delayprint("test?")
delayprint("ok boomer", delay=0.25)
delayprint('...', delay=1)