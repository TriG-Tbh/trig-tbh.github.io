from PIL import Image
import random
import os
import sys


def clear():
    import platform
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass


clear()

method = input("Method\n1: Classic\n2: Instant Gradient\nPick a method: ")
clear()
try:
    method = int(method)
except:
    print("Cannot convert to integer: " + method)
    sys.exit(1)
if method != 1 and method != 2:
    print("Invalid method: " + str(method))
    sys.exit(1)

if method == 1:
    width = input("Width of image (pixels): ")
    try:
        width = int(width)
    except:
        print("Cannot convert to integer: " + width)
        sys.exit(1)
    if width < 1:
        print("Width must be at least 1")
        sys.exit(1)

    height = input("Height of image (pixels): ")
    try:
        height = int(height)
    except:
        print("Cannot convert to integer: " + height)
        sys.exit(1)
    if height < 1:
        print("Height must be at least 1")
        sys.exit(1)

    basecolor = input(
        "Initial color (three values separated by \", \", leave blank for random): ")
    try:
        r, g, b = basecolor.split(", ")
    except:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
    else:
        r, g, b = int(r), int(g), int(b)
    basecolor = (r, g, b)
elif method == 2:
    imagepath = input("Path to image file: ")
    try:
        open(imagepath, 'r')
    except IOError:
        print("Invalid path: " + imagepath)
        sys.exit(1)


global seed
seed = input("Seed (randomness) of image: ")
try:
    seed = int(seed)
except:
    print("Cannot convert to integer: " + seed)
    sys.exit(1)
if seed < 1:
    print("Seed must be at least 1")
    sys.exit(1)

clear()
if method == 1:
    print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(
        width, height, seed, basecolor))
    image = Image.new("RGB", (width, height))
    pixels = image.load()
    pixels[0, 0] = basecolor
elif method == 2:
    print("Image path: {}\nSeed: {}".format(imagepath, seed))
    image = Image.open(imagepath)
    image = image.convert("RGBA")
    pixels = image.load()
print("Building image...")

if method == 1:
    def alter(base):
        new = ()
        for value in base:
            new = list(new)
            newvalue = value + random.randint(-seed, seed)
            if newvalue > 255:
                newvalue = 255 - (value - 255)
            elif newvalue < 0:
                newvalue = 0 + (0 - value)
            new.append(newvalue)
        new = tuple(new)
        return new
elif method == 2:
    def alter(base):
        new = ()
        new = list(new)
        for i in range(3):
            new.append(base[i])
        value = base[3]
        newvalue = value + random.randint(-seed, seed)
        if newvalue > 255:
            newvalue = 255 - (value - 255)
        elif newvalue < 0:
            newvalue = 0 + (0 - value)
        new.append(newvalue)
        new = tuple(new)
        return new

for w in range(image.width):
    for h in range(image.height):
        if method == 1:
            base = (0, 0, 0)
        elif method == 2:
            base = (0, 0, 0, 0)

        # If pixel is top left
        if w == 0 and h == 0:
            pass
        # If pixel is on left edge
        elif w == 0:
            if method == 1:
                base = pixels[w, h - 1]
                new = alter(base)
                pixels[w, h] = new
            elif method == 2:
                base = pixels[w, h]
                new = alter(base)
                pixels[w, h] = new
        # If pixel is on top edge
        elif h == 0:
            if method == 1:
                base = pixels[w - 1, h]
                new = alter(base)
                pixels[w, h] = new
            elif method == 2:
                base = pixels[w, h]
                new = alter(base)
                pixels[w, h] = new
        else:
            above = pixels[w, h - 1]
            side = pixels[w - 1, h]
            upleft = pixels[w - 1, h - 1]
            if method == 1:
                added = [0, 0, 0]
            index = 0
            if method == 1:
                averaged = []
                for value in above:
                    added[index] += value
                    index += 1
                index = 0
                for value in side:
                    added[index] += value
                    index += 1
                index = 0
                for value in upleft:
                    added[index] += value
                    index += 1
                for item in added:
                    average = int(round(item / 3, 0))
                    averaged.append(average)
            elif method == 2:
                added = 0
                added += above[3]
                added += side[3]
                added += upleft[3]
                averagea = int(round(added / 3, 0))
                base = list(pixels[w, h]).copy()
                base[3] = averagea
                averaged = base.copy()
                averaged = tuple(averaged)
            new = alter(averaged)
            try:
                pixels[w, h] = new
            except:
                print(averaged)
                print(new)
                print(w)
                print(h)
                input()

clear()

print("Image successfully built.")
if method == 1:
    print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(
        width, height, seed, basecolor))
elif method == 2:
    print("Image path: {}\nSeed: {}".format(imagepath, seed))
dirpath = os.path.realpath(os.path.dirname(__file__))
name = input("File will be saved to: " + dirpath +
             " (.png file format)\nGive a name for your artwork: ")

try:
    path = os.path.join(dirpath, name + ".png")
    image.save(path)
except Exception as e:
    print("Exception occured while saving: " + str(e))
else:
    clear()
    print("File saved to: " + path)
    if method == 1:
        print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(
            width, height, seed, basecolor))
    elif method == 2:
        print("Image path: {}\nSeed: {}".format(imagepath, seed))
