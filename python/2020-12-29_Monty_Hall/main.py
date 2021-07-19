import random

random.seed(875263487)

iterations = 500

def doors(swap=False):
    options = [0] * 3
    options[random.randint(0, 2)] = 1
    zeroed = []
    choice = random.randint(0, 2)
    for i in range(3):
        if options[i] == 0:
            zeroed.append(i)
    temp = zeroed.copy()
    if choice in zeroed:
        del temp[temp.index(choice)]
    else:
        del temp[random.randint(0, 1)]
    options[temp[0]] = "open"
    if not swap:
        return options[choice] == 1
    removed = [i for i in range(3)]
    del removed[removed.index(options.index("open"))]
    del removed[removed.index(choice)]
    return options[removed[0]] == 1

final = {
    True: [0, 0],
    False: [0, 0]
}

for swap in [True, False]:
    for i in range(iterations):
        won = doors(swap=swap)
        if won:
            final[swap][0] += 1
        else:
            final[swap][1] += 1

for item in final:
    games = final[item]
    print("{}: {} / {} ({}%)".format(item, games[0], games[0] + games[1], round((games[0] / (games[0] + games[1])) * 100, 4)))
