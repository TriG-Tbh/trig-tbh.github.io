firstnum = int(input("Enter the first number: "))
secondnum = int(input("Enter the second number: "))

divnum = 1
modnum = 0

firstfactors = []
secondfactors = []
finalfactors = []

for i in range(1, firstnum + 1):
    modnum = firstnum % divnum
    if modnum == 0:
        firstfactors.append(divnum)
    divnum = divnum + 1

divnum = 1
modnum = 0

for i in range(1, secondnum + 1):
    modnum = secondnum % divnum
    if modnum == 0:
        secondfactors.append(divnum)
    divnum = divnum + 1

checknum1 = 0

for i in range(1, len(firstfactors)+1):
    checknum2 = 0
    for i in range(1, len(secondfactors)+1):
        if firstfactors[checknum1] == secondfactors[checknum2]:
            finalfactors.append(firstfactors[checknum1])
        checknum2 += 1
    checknum1 += 1
finalnum = int((finalfactors[len(finalfactors) - 1]))

finalfirst = str(int(firstnum / finalnum))
finalsecond = str(int(secondnum / finalnum))
firstnum = str(firstnum)
secondnum = str(secondnum)

print(firstnum + " and " + secondnum + " can both be divided by " + str(finalnum))
print(firstnum + " can be reduced to " + finalfirst + ", while " + secondnum + " can be reduced to " + finalsecond)
