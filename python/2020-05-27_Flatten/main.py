from PIL import Image
import os
import math


def clear():
    import platform
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass


def difference(c1, c2):
    return math.sqrt(((c2[0] - c1[0])**2) + ((c2[1] - c1[1])**2) +
                     ((c2[2] - c1[2])**2))


clear()

imagepath = input("Path: ")
limit = input("Limit of colors: ")
limit = int(limit)
clear()
image = Image.open(imagepath)
image = image.convert("RGBA")
print("Loading image...")
pixels = image.load()
print("Building palette...")
palette = {}

for w in range(image.width):
    for h in range(image.height):
        if pixels[w, h] not in palette.keys():
            palette[pixels[w, h]] = 1
        else:
            palette[pixels[w, h]] += 1

print("Sorting palette...")
palette = {
    k: v
    for k, v in sorted(palette.items(), key=lambda item: item[1], reverse=True)
}

palette = {k: palette[k] for k in list(palette.keys())[:limit]}

print("Building new image...")
new = Image.new("RGBA", (image.width, image.height))
npixels = new.load()

for w in range(image.width):
    for h in range(image.height):
        color = pixels[w, h]
        closest = ()
        dif = math.inf
        for oldcolor in palette.keys():
            if difference(color, oldcolor) < dif:
                closest = oldcolor
                dif = difference(color, oldcolor)
        npixels[w, h] = closest

dirpath = os.path.realpath(os.path.dirname(__file__))
clear()
name = input("Filename to save to (.png): ")
try:
    path = os.path.join(dirpath, name + ".png")
    new.save(path)
except Exception as e:
    print("Exception occured while saving: " + str(e))
else:
    print("File successfully saved.")