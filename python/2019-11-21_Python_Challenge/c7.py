from PIL import Image

image = Image.open("/home/trig/Downloads/oxygen.png")

width, height = image.size

print("".join([chr(image.getpixel((i, height//2))[0]) for i in range(0, width, 7)]))
print("".join(map(chr, [105, 110, 116, 101, 103, 114, 105, 116, 121])))