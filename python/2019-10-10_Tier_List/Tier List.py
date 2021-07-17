import os
tiers = {"S": [], "A": [], "B": [], "C": [], "D": [], "F": []}

os.system("clear")


while True:
    os.system("clear")
    name = input("Name of movie (press enter to exit): ")
    if name == "":
        break
    year = input("Year of release: ")
    try:
        year = int(year)
    except:
        input("Invalid year. Press enter to continue. ")
        continue
    tier = input("Tier: ")
    if tier.lower() not in ['s', 'a', 'b', 'c', 'd', 'f']:
        input("Tier not recognized. Press enter to continue. ")
        continue
    tier = tier.upper()
    tiers[tier].append((name, year))

os.system("clear")
output = ""
for item in tiers:
    joined = ""
    for tup in tiers[item]:
        
    joined = 
    string = ", ".join()