import requests
from bs4 import BeautifulSoup
import re
import os

os.system("clear")

searchterm = input("Searchterm: ")
os.system("clear")

resp = requests.get("https://store.steampowered.com/search/?term={}".format(searchterm))
soup = BeautifulSoup(resp.content, features='html.parser')
try:
    applink = [l.get('href') for l in soup.findAll('a') if "store.steampowered.com/app/" in l.get('href')][2]
except:
    print("Game not found")
    exit()

resp = requests.get(applink)

soup = BeautifulSoup(resp.content, features="html.parser")

name_div = soup.find("div", class_="apphub_AppName")
name = name_div.text.lstrip().strip()

discount = soup.find('div', class_='discount_pct')
if discount is None:
    price_div = soup.find('div', class_='game_purchase_price price')
    price = price_div.text.lstrip().strip()
    print("Game: {}".format(name))
    print("Price: {}".format(price))
else:
    discount_percent = discount.text.lstrip().strip()[1:]
    orig_price_div = soup.find('div', class_='discount_original_price')
    original_price = orig_price_div.text.lstrip().strip()
    new_price_div = soup.find('div', class_='discount_final_price')
    new_price = new_price_div.text.lstrip().strip()

    print("Game: {}".format(name))
    print("DISCOUNT: {}".format(discount_percent))
    print("Original price: {}".format(original_price))
    print("New price: {}".format(new_price))