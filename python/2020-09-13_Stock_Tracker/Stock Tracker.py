import requests
import bs4

def chunk(l, n):
    x = [l[i:i + n] for i in range(0, len(l), n)]
    return x

stocks = {}

for i in range(10):
    i += 1
    
    url = "https://markets.businessinsider.com/index/s&p_500?p=" + str(i)

    content = requests.get(url).content
    soup = bs4.BeautifulSoup(content)
    texts = soup.find_all("td", class_="table__td")
    
    chunks = chunk(texts, 5)

    for chunk in chunks:
        name = chunk[0].split("\n")[1].split("\">")[1].split("</a>")[0]
        ticker = chunk[0].split("\n")[1].split("href=\"/stocks/")[1].split("-stock/")[0].upper()
        close = chunk[1].split("\n")[1].strip("</td>").strip()
        last = chunk[2].split("\n")[1].split(">")[2].split("</")[0]
        gain = chunk[3].