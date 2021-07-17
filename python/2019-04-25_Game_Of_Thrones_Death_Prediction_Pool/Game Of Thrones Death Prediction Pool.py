characters = ["Jon Snow", "Arta Stark", "Euron Greyjoy",
"Brienne of Tarth", "Berie Dondarrion", "Melisandre",
"Robin Arryn", "Hot Pie", "Daenerys Targaryen",
"Sansa Stark", "Samwell Tarly", "Tormund",
"Grey Worm", "Eddison Tollet", "Yohn Royce",
"Drogon", "Tyronion Lannister", "Bran Stark",
"Gilly", "Sandor Clegane", "Missandei",
"Podrick", "Lyanna Mormont", "Rhaegal",
"Jaime Lannister", "Theon Greyjoy", "Bronn",
"Gregor Clegane", "Gendry", "Dario Naharis",
"Meera Reed", "Viserion", "Cersei Lannister",
"Yara Greyjoy", "Davos Seaworth", "Jorah Mormont",
"Varys", "Qyburn", "Edmure Tully",
"The Night King"]

saves = {} # The top (threshold, described below) characters will be saved

for char in characters:
    saves[char] = 0

import random

threshold = 0 # Threshold determines the amount of people that will stay alive.
for i in range(73): # Number is how many episodes of GoT there are in total (aired and unaired)
    threshold += random.randint(10, 24)
threshold = threshold // 73 # Whatever number is returned is how many will survive season 8

'''TEST ONE [EDUCATED]: GOOGLE RESULTS
In this test, all characters are searched on fandom.com.
The 90% of characters that have the longest articles
get one point added to their "Save" counter.'''
lengths = {}
for char in characters:
    from bs4 import BeautifulSoup
    from bs4 import BeautifulSoup as bs
    import requests
    import re
    query = char.replace(" ", "_")
    html = requests.get("https://gameofthrones.fandom.com/wiki/" + query).content
    unicode_str = html.decode("utf8")
    encoded_str = unicode_str.encode("ascii",'ignore')
    news_soup = BeautifulSoup(encoded_str, "html.parser")
    a_text = news_soup.find_all('p')
    y = [re.sub(r'<.+?>',r'',str(a)) for a in a_text]
    fullstring = ""
    for text in y:
        fullstring += text
    lengths[char] = len(fullstring)
lengths = sorted(lengths.items(), key=lambda x:x[1], reverse=True)
for i in range(4):
    del lengths[-i - 1]
for char in lengths:
    saves[char[0]] += 1
    
