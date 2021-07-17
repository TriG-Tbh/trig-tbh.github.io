# Right to Space

import pynput
from pynput import mouse
from pynput.mouse import Button
import pyautogui


def on_click(x, y, button, pressed):
    if str(button) == "Button.right":
        pyautogui.press('space')


with mouse.Listener(
        on_click=on_click) as listener:
    listener.join()
