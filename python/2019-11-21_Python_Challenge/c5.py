import pickle
from urllib.request import urlopen

with urlopen("http://www.pythonchallenge.com/pc/def/banner.p") as w:
    biglist = pickle.load(w)

for line in biglist:
    printline = []
    for item in line:
        printline.append(item[0] * item[1])
    print("".join(printline))
