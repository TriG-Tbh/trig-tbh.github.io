import bs4
import requests
import os
os.system("clear")

gunsurl = "https://enterthegungeon.gamepedia.com/Guns"

page = requests.get(gunsurl)
soup = bs4.BeautifulSoup(page.content, "html.parser")

for br in soup.find_all("br"):
    br.replace_with("\n")

quality = {
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/b/bf/N_Quality_Item.png?version=d62d33ff747269340a2786d0bc707fb9": "N/A",
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/6/60/D_Quality_Item.png?version=484e9441ad7b8bba2da4079c5984bf99": "D",
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/b/bd/C_Quality_Item.png?version=3f82a0b3849e9989060cbd03062b8780": "C",
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/f/f3/B_Quality_Item.png?version=99613a5f83c53195e09b42773b351676": "B",
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/9/9c/A_Quality_Item.png?version=24c0812d903d9ffb91704eb9ec8c4e5b": "A",
    "https://gamepedia.cursecdn.com/enterthegungeon_gamepedia/8/8b/1S_Quality_Item.png?version=40a22e5d15d51edf8172d87fc8288f9f": "S"
}

guns = {}

gunlisting = soup.find_all('tr')[1:]
for gun in gunlisting:
    entries = gun.find_all("td")
    information = {
        "Name": entries[1].text.strip(),
        "Quote": entries[2].text.strip(),
        "Quality": quality[entries[3].find("img")["src"]],
        "Type": entries[4].text.strip(),
        "Magazine Size": (entries[5].text.strip() if entries[5].find("img") is not None else "∞") + " bullets",
        "Ammo Capacity": (entries[6].text.strip() if entries[6].find("img") is not None else "∞") + " bullets",
        "Damage": entries[7].text.strip().replace("\n", "damage per bullet, ") + " damage per bullet",
    }
    print(information)
    input()
    os.system("clear")