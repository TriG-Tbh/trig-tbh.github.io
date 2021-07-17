from pynput.keyboard import Key, Listener
import os

global previous
previous = ""

shiftdict = {
    "`": "~",
    "1": "!",
    "2": ""
}

def on_press(key):
    character = str(key)
    if character[0] == "\"" and character[1] == "'":
        key = "'"
    else:
        key = character.replace("'", "")
    print(key)

with Listener(on_press=on_press) as listener:
        listener.join()
