from PIL import Image, ImageChops

def trim(im, remove):
    bg = Image.new(im.mode, im.size, remove)
    diff = ImageChops.difference(im, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return im.crop(bbox)

basepath = "/home/trig/Downloads/santahat2.png"
referencepath = "/home/trig/Downloads/natalieportman.jpeg"
savepath = "/home/trig/test2.png"

baseimage = Image.open(basepath)
#baseimage = baseimage.convert("RGBA")
referenceimage = Image.open(referencepath)

def getaverage(image):
    pixels = image.load()
    width, height = image.size
    average = [0, 0, 0]
    for x in range(width):
        for y in range(height):
            if len(pixels[x, y]) > 3:
                r, g, b, _ = pixels[x, y]
            else:
                r, g, b = pixels[x, y]
            average[0] += r
            average[1] += g
            average[2] += b
    average = [int(round(i/(width * height), 0)) for i in average]
    return average

def getdifference(avg1, avg2):
    difference = []
    for i in range(len(avg1)):
        difference.append(avg1[i] - avg2[i])
    return difference

def getgsdif(avg1, avg2):
    avg1 = [int(round(avg1[0] * 0.2989)), int(round(avg1[1] * 0.5870)), int(round(avg1[2] * 0.1140))]
    avg2 = [int(round(avg2[0] * 0.2989)), int(round(avg2[1] * 0.5870)), int(round(avg2[2] * 0.1140))]
    difference = []
    for i in range(len(avg1)):
        difference.append(avg1[i] - avg2[i])
    return difference

def alter(difference, color):
    for i in range(3):
        color[i] = color[i] + difference[i]
    for i in range(len(color)):
        if color[i] < 0:
            newc = color[i]
            color = [item + abs(newc) for item in color]
        if color[i] > 255:
            newc = color[i]
            color = [item - (newc - 255) for item in color]
    return tuple(color)

baseaverage = getaverage(baseimage)
referenceaverage = getaverage(referenceimage)
difference = getgsdif(baseaverage, referenceaverage)

def apply_difference(difference, image, savepath):

    #image = trim(image, alter(difference, [255, 255, 255]))
    #image.show()
    pixels = image.load()
    width, height = image.size
    #newimg = Image.new()
    #print(alter(difference, [255, 255, 255]))
    #plist = [pixels[x, y] for y in range(height) for x in range(width)]
    #print(alter(difference, [255, 255, 255]) in plist)
    #input()
    #print((255, 255, 255) in plist)
    for x in range(width):
        for y in range(height):
            #print(pixels[x, y])
            #input()
            if len(pixels[x, y]) > 3:
                if pixels[x, y] == (0, 0, 0, 0):
                    continue
                #if pixels[x, y] == alter(difference, [255, 255, 255]):
                #    pixels[x, y] = (0, 0, 0, 0)
                #    continue
                r, g, b, _ = pixels[x, y]
                color = [r, g, b]
                #distance = []
                
            else:
                color = pixels[x, y]
            list_a = color.copy()
            diffs = []
            for i, e in enumerate(list_a):
                for j, f in enumerate(list_a):
                    if i != j: 
                        diffs.append(abs(e-f))
            if sum(diffs)/len(diffs) < 3:
                pixels[x, y] = (0, 0, 0, 0)
                continue
            color = alter(difference, list(color))
            #if len(pixels[x, y]) > 3:
            #    color.append(0)    
            pixels[x, y] = tuple(color)
    image.save(savepath, "PNG")

apply_difference(difference, baseimage, savepath)