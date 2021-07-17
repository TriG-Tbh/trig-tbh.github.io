from pynput.mouse import Button, Controller
from pynput import keyboard
from pynput.keyboard import Key

mouse = Controller()

def on_press(key):
    if key == Key.shift_r:
        while True:
            mouse.click(Button.left)


with keyboard.Listener(
        on_press=on_press
        ) as listener:
    listener.join()