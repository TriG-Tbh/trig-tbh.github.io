from urllib.request import urlopen

baseurl = "http://www.pythonchallenge.com/pc/def/linkedlist.php?nothing="
nothing = "8022"

blacklist = []
blacklist.append(nothing)

while True:
    url = baseurl + nothing
    with urlopen(url) as response:
        html = response.read()
    html = html.decode("utf-8")
    nothing = html.split(" ")[-1]
    try:
        _ = int(nothing)
    except:
        print(nothing)
        break
    if nothing in blacklist:
        print[blacklist[-1]]
        break
    blacklist.append(nothing)
    print(nothing)