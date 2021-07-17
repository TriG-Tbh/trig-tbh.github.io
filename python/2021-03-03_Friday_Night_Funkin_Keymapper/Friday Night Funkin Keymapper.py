from pynput import keyboard
from pynput.keyboard import Key, Controller

controller = Controller()

import win32gui
import win32con
import win32api

hwndMain = win32gui.FindWindow(None, "Friday Night Funkin'")
print(hwndMain)
hwndChild = win32gui.GetWindow(hwndMain, win32con.GW_CHILD)

import pyautogui
def on_press(key):
    keys = ["h", "j", "k", "l"]
    key = str(key)
    print(key == "'{}'".format(keys[0]))
    if key == "'{}'".format(keys[0]):
        temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x25, 0x001E0001)
    if key == "'{}'".format(keys[1]):
        temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x28, 0x001E0001)
    if key == "'{}'".format(keys[2]):
        temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x26, 0x001E0001)
    if key == "'{}'".format(keys[3]):
        temp = win32api.PostMessage(hwndChild, win32con.WM_CHAR, 0x27, 0x001E0001)
    print(temp)
    
def on_release(key):
    pass

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

