import os
basepath = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(basepath, "file1.mp3"), "rb") as f:
    file1bytes = f.read()

def closest(l, K): 
    return l[min(range(len(l)), key=lambda i: abs(l[i]-K))] 

with open(os.path.join(basepath, "file2.mp3"), "rb") as f:
    file2bytes = f.read()

writtenbytes = []

unique = []

deviated = False
deviationpoint = None

for i in range(len(file1bytes)):
    if i % 1024 == 0:
        #print(i // 1024)
        pass
    b1 = file1bytes[i]
    b2 = file2bytes[i]
    if b1 == b2:
        writtenbytes.append(b1)
    elif b1 != b2:
        if deviationpoint is None:
            deviationpoint = i
        if unique == []:
            unique = list(set(file2bytes[deviationpoint:]))
        b3 = closest(unique, b1)
        writtenbytes.append(b3)

with open(os.path.join(basepath, "file3.mp3"), "wb") as f:
    f.write(bytes(writtenbytes))
