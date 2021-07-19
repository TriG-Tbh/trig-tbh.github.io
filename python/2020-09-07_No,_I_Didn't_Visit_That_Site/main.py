from bs4 import BeautifulSoup

import requests

url = input("Target URL: ")

content = requests.get(url)

read_content = content.content

print(read_content)

soup = BeautifulSoup(read_content,'html.parser')

pAll = soup.find_all('p')

for item in pAll:
    print(item.text)