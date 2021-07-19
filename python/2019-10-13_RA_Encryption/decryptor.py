import platform
import os
import sys


def clear():
	if platform.system() == "Windows":
		os.system('cls')
	if platform.system() == "Linux":
		os.system("clear")

keys = []

key = "None"
while key != "":
    clear()
    if len(keys) != 0:
        for key in keys:
            print(key)
    key = input("Enter a key: ")
    if key == "":
        break
    if len(key) != 95:
        input("Invalid key. Press enter to continue. ")
        continue
    keys.append(key)

keys = keys[::-1].copy()

clear()

result = input("Enter the encrypted text: ")
clear()