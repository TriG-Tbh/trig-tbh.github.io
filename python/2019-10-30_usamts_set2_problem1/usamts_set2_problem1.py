ilist = [1, 2, 3, 4, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
lists = []
for _ in range(len(ilist)):
    newlist = ilist[-1:] + ilist[:-1]
    newlist.append(5)
    lists.append(newlist)
    ilist = ilist[-1:] + ilist[:-1]

lists = lists[::-1]

from multiprocessing import Process

def getabcd(list, start):
    a = list[start]
    b = list[start + 1]
    c = list[start + 4]
    d = list[start + 5]
    return a, b, c, d

def permutation(list, start, end, beginning):
    '''This prints all the permutations of a given list
       it takes the list,the starting and ending indices as input'''
    if (start == end):
        if beginning != list[0]:
            exit()
        a, b, c, d = getabcd(list, 1)
        if (a + c) * (b + d) == 638:
            a, b, c, d = getabcd(list, 2)
            if (a + c) * (b + d) == 650:
                a, b, c, d = getabcd(list, 4)
                if (a + c) * (b + d) == 50:
                    a, b, c, d = getabcd(list, 6)
                    if (a + c) * (b + d) == 338:
                        a, b, c, d = getabcd(list, 8)
                        if (a + c) * (b + d) == 77:
                            a, b, c, d = getabcd(list, 9)
                            if (a + c) * (b + d) == 130:
                                if list[-1] == 5:
                                    print(list)
                                    exit()
    else:
        for i in range(start, end + 1):
            list[start], list[i] = list[i], list[start]  # The swapping
            permutation(list, start + 1, end, beginning)
            list[start], list[i] = list[i], list[start]

for list in lists:
    print("Now starting on:\n{}".format(list))
    beginning = list[0]
    newpermutation = Process(target=permutation, args=(list, 0, len(list) - 1, beginning,))
    newpermutation.start()
    newpermutation.join()