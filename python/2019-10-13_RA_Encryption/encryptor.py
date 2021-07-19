import random
import platform
import os
import sys

def clear():
	if platform.system() == "Windows":
		os.system('cls')
	if platform.system() == "Linux":
		os.system("clear")


characters = """QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm `1234567890-=~!@#$%^&*()_+[]\\{}|;':",./<>?"""

clear()

keys = []

try:
    string = input("Enter string to be encrypted: ")
    layers = input("Enter the amount of times you want your message to be encrypted: ")
except Exception as e:
    clear()
    try:
        input("Exception occured: {}. Press enter to continue. ".format(str(e)))
    except:
        pass
    finally:
        clear()
        sys.exit(1)

try:
    layers = int(layers)
except:
    clear()
    try:
        input("Invalid number inputted. Press enter to continue. ")
    except:
        pass
    finally:
        clear()
        sys.exit(1)

clear()
characters = list(characters)
new = string

keys.append(characters)

x = 0

for i in range(layers):
    key = characters.copy()
    while True:
        random.shuffle(key)
        if key != characters:
            break
    keys.append(key)
    ciphered = ""
    for character in new:
        if character in key:
            ciphered += key[keys[x].index(character)]
        else:
            ciphered += character
    ciphered = "".join(ciphered)
    new = ciphered
    x += 1

clear()
print("Keys (from first to last): ")
for key in keys:
    print("".join(key))
print("\n" + "Comparison: ")
print(string + "\n")
print(new)