import random
def alter(base, seed):
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