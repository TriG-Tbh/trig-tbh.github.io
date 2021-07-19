import urllib.request
import json
from datetime import datetime
import sys
import os
import platform
import pytz
import time
import csv


global key
key = "[REDACTED]"

def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        if platform.system() == "Darwin" and platform.machine().startswith("iP"):
            try:
                import console
                console.clear()
            except ImportError:
                pass


def get_endpoint(endpoint, key=None):
    if key is not None:
        endpoint = endpoint + "?key=" + key
    with urllib.request.urlopen("https://api.hypixel.net" + endpoint) as request:
        data = request.read().decode()
        return data
    return None


def load_auctions():
    global key
    auction_house = get_endpoint("/skyblock/auctions?key=" + key)

    for char in "0123456789abcdef":
        replace = "§" + char
        auction_house = auction_house.replace(replace, "")

    auction_house = json.loads(auction_house)

    auctions = auction_house["auctions"]
    return auctions

def convert_time(timestamp):
    timestamp /= 1000
    utc_dt = datetime.utcfromtimestamp(timestamp)
    aware_utc_dt = utc_dt.replace(tzinfo=pytz.utc)
    tz = pytz.timezone("America/Los_Angeles")
    dt = aware_utc_dt.astimezone(tz)
    return dt


def is_valid_time(timestamp, pickup_times):
    dt = convert_time(timestamp)
    hour = int(dt.strftime("%H"))
    for hourset in pickup_times:
        if hourset[0] <= hour < hourset[1]:
            return True
    return False



def search(tiers, pickup_times, categories):
    global key
    auctions = load_auctions()
    auctions = [auction for auction in auctions if is_valid_time(auction["end"], pickup_times)]
    
    


    auctions = [auction for auction in auctions if auction["tier"] in tiers]
    auctions = [auction for auction in auctions if auction["category"] in categories]
    for auction in auctions:
        auctioneer_uuid = auction["auctioneer"]
        resp = json.loads(get_endpoint(f"/player?uuid={auctioneer_uuid}&key={key}"))
        auction["player_name"] = resp["player"]["playername"]
        auction["datetime"] = convert_time(auction["end"]).strftime("%m/%d/%Y at %H:%M:%S")
        try:
            highest = max([bid["amount"] for bid in auction["bids"]])
        except:
            highest = 0
        auction["highest_bid"] = highest


    auctions = [{"name": auction["item_name"], "seller": auction["player_name"], "rarity": auction['tier'], "lore": auction['item_lore'], "highest_bid": auction['highest_bid'], "end": auction["datetime"]} for auction in auctions]
    return auctions



def main():
    clear()
    tiers = []
    while True:
        clear()
        print("Target tiers: " + ", ".join(tiers))
        tier = input("Tier to add (COMMON - SPECIAL): ")
        if tier == "":
            break
        tier = tier.upper()
        if tier not in ["COMMON", "UNCOMMON", "RARE", "EPIC", "LEGENDARY", "MYTHIC", "SPECIAL"]:
            continue
        if tier not in tiers:
            tiers.append(tier)
    clear()
    timestr = []
    times = []
    while True:
        clear()
        print("Target end times: " + ", ".join(timestr))
        start = input("Start of pickup window (0-23 hours): ")
        if start == "":
            break
        end = input("End of pickup window (0-23 hours): ")
        if end == "":
            break
        try:
            start, end = int(start), int(end)
        except:
            continue
        if not (0 <= start <= 23) or not (0 <= end <= 23):
            continue
        if f"{start} - {end}" not in timestr and (start, end) not in times:
            timestr.append(f"{start} - {end}")
            times.append((start, end))
    clear()
    categories = []
    while True:
        clear()
        print("Categories: " + ", ".join(categories))
        cat = input("Category to add: ")
        if cat == "":
            break
        cat = cat.lower()
        if cat not in ["weapon", "blocks", "armor", "accessories", "consumables", "misc"]:
            continue
        if cat not in categories:
            categories.append(cat)
    clear()
    print("Tiers: " + ", ".join(tiers))
    print("Pickup windows: " + ", ".join(timestr))
    print("Categories: " + ", ".join(categories))
    confirm = input("Confirm (Y/N)? ")
    if not confirm.lower().startswith("y"):
        sys.exit(1)
    
    clear()

    auctions = search(tiers, times, categories)
    print(len(auctions))

    timestamp = convert_time(time.time() * 1000).strftime("%m-%d-%Y, %H-%M-%S")
    savefolder = r"C:\Users\ms_lu\Downloads"

    with open(os.path.join(savefolder, timestamp + ".csv"), "w", newline='', encoding="utf-8-sig") as outputfile:
        fc = csv.DictWriter(outputfile, fieldnames=auctions[0].keys())
        fc.writeheader()
        fc.writerows(auctions)

    
if __name__ == "__main__":
    main()