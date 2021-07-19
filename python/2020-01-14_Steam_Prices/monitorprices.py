import requests
import json
import pickle

import pandas as pd
import numpy as np
import scipy.stats as sci

from datetime import datetime
import time
import random

key = {"steamLoginSecure": "[REDACTED]"}

gamelist = []

for gameid in gamelist:
    allitemnames = []
    allitemsget = requests.get('https://steamcommunity.com/market/search/render/?search_descriptions=0&sort_column=default&sort_dir=desc&appid={}&norender=1&count=100'.format(gameid), cookies=cookie)
    allitems = allitemsget.content

    allitems = json.loads(allitems)
    totalitems = allitems['total_count']
    print()