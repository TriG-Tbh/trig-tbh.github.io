from PIL import Image
import random
import os, sys
os.system("clear")

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


basecolor = input("Initial color (three values separated by \", \", leave blank for random): ")
try:
    r, g, b = basecolor.split(", ")
except:
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
else:
    r, g, b = int(r), int(g), int(b)

basecolor = (r, g, b)

os.system("clear")
print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(width, height, seed, basecolor))
print("Building image...")


def alter(base):
    new = ()
    value = base[0]
    new = list(new)
    newvalue = value + random.randint(-seed, seed)
    if newvalue > 255:
        newvalue = 255 - (value - 255)
    elif newvalue < 0:
        newvalue = 0 + (0 - value)
    for i in range(3):
        new.append(newvalue)
    new = tuple(new)
    return new
            
image = Image.new("RGB", (width, height))
pixels = image.load()
pixels[0, 0] = basecolor

for w in range(image.width):
    for h in range(image.height):
        base = (0, 0, 0)
        # If pixel is top left
        if w == 0 and h == 0:
            pass
        # If pixel is on left edge
        elif w == 0:
            base = pixels[w, h - 1]
            new = alter(base)
            pixels[w, h] = new
        # If pixel is on top edge
        elif h == 0:
            base = pixels[w - 1, h]
            new = alter(base)
            pixels[w, h] = new
        else:
            above = pixels[w, h - 1]
            side = pixels[w - 1, h]
            upleft = pixels[w - 1, h - 1]
            added = [0, 0, 0]
            averaged = []
            index = 0
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
            new = alter(averaged)
            pixels[w, h] = new
            
os.system("clear")

print("Image successfully built.")
print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(width, height, seed, basecolor))
dirpath = os.path.realpath(os.path.dirname(__file__))
name = input("File will be saved to: " + dirpath + " (.png file format)\nGive a name for your artwork: ")

try:
    image.save(dirpath + "/" + name + ".png")
except Exception as e:
    print("Exception occured while saving: " + str(e))
else:
    os.system("clear")
    print("File saved to: " + dirpath + "/" + name + ".png")
    print("Width: {}\nHeight: {}\nSeed: {}\nInitial color: {}".format(width, height, seed, basecolor))
