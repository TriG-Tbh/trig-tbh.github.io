from functions import alter
def topleftbottomright(pixels, width, height):
    for w in range(width):
        for h in range(height):
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
                for item in added:
                    average = int(round(item / 2, 0))
                    averaged.append(average)
                new = alter(averaged)
                pixels[w, h] = new
                