import os
import sys
import random
import time

def clear():
    import platform
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass

characters = []
clear()
while True:
    option = input("1: Manually input characters one by one\n2: Input a batch of characters\nPick an option: ")
    try:
        option = int(option)
    except:
        continue
    if option not in [1, 2]:
        continue
    else:
        break
if option == 1:
    while True:
        clear()
        print("Characters: " + ", ".join(characters))
        try:
            c = input("New character (Ctrl+C to remove last entry): ")
        except KeyboardInterrupt:
            if len(characters) >= 1:
                del characters[-1]
            continue
        if c.strip().lstrip() == "":
            break
        characters.append(c)
else:
    clear()
    characters = input("Characters (separate characters with \", \"): ").strip().lstrip().split(", ")

random.seed(9871421)

random.shuffle(characters)

mapped = {}

for c in characters:
    mapped[str(characters.index(c) / len(characters) * 100)] = c

clear()

while True:
    question = input("Question: ")
    question = question.lower()
    alphabet = "qwertyuiopasdfghjklzxcvbnm1234567890"
    question = "".join(sorted([l for l in question if l in alphabet]))
    value = abs(hash(question)) % (10 ** 2)
    indexes = list(mapped.keys())[::-1]
    smallest = [i for i in indexes if float(i) <= value][0]
    for i in range(3):
        sys.stdout.write(".")
        sys.stdout.flush()
        time.sleep(0.75)
    print("\rAnswer: " + mapped[smallest] + "\n")
    