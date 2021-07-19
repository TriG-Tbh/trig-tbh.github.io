link = "/home/trig/Downloads/channel (1).zip"

import zipfile

nothing = "90052"

blacklist = []
comments = []
blacklist.append(nothing)

f = zipfile.ZipFile(link)



while True:

    content = f.read(nothing + ".txt").decode("utf-8")
    comments.append(f.getinfo(nothing + ".txt").comment.decode("utf-8"))
    nothing = content.split(" ")[-1]
    try:
        _ = int(nothing)
    except:
        #print(nothing)
        break
    if nothing in blacklist:
        #print[blacklist[-1]]
        break
        
    blacklist.append(nothing)


    #print(nothing)

print("".join(comments))
