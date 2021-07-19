from ebooklib import epub
import bs4, requests
from PIL import Image
import io

book = epub.EpubBook()


volume = input("Volume: ")
name = "Attack on Titan Vol. " + volume

book.set_title(name)
book.set_language('en')
book.set_direction("rtl")

author = "Hajime Isayama"

book.add_author(author)


chapter_prefix = "https://readshingekinokyojin.com/manga/shingeki-no-kyojin-chapter-"

 

coverresp = requests.get("https://attackontitan.fandom.com/wiki/List_of_Attack_on_Titan_chapters")
soup = bs4.BeautifulSoup(coverresp.content, features="lxml")
for img in soup.findAll('img'):
    url = img.get('src')
#cover_art = [img.get('href') for img in soup.findAll("a") if "Volume_" + volume in img.get("href")]
links = [x.get("href") for x in soup.findAll("a") if x.get("href") is not None]
cover = ""

cover = [c for c in links if ("Volume_" + volume) in c][0]


initial = [td for td in soup.findAll("td") if hasattr(td, "text")]
td = [t for t in initial if t.text.strip().lstrip() == volume.strip().lstrip()]
ol = td[0].parent.parent.find("ol")
start = str(ol).split("\n")[0].split("start=\"")[1].split("\"")[0] # string trickery 1
end = str(int(start) + int(len(str(ol).strip().split("\n"))) - 1) # string trickery 2

ignore_first = (True if input("Remove first page of every chapter (y/n)? ").lower().lstrip().startswith("y") else False)

chapternames = [f"Chapter {int(start) + i}" for i in range(int(end) - int(start) + 1)]

chapters = []
toc = []

ei = epub.EpubImage()
ei.file_name = "cover.jpeg"
ei.media_type = 'image/jpeg'
resp = requests.get(cover)
ei.content = resp.content
#book.add_item(ei)
book.set_cover("EPUB/cover.jpeg", resp.content, False)


#print(book.spine)


cstr = [str(c) for c in range(int(start), int(end) + 1)]

book.spine = []

cstr = [str(c) for c in range(int(start), int(end) + 1)]
i = 0
print(chapternames)
for cname in chapternames:
    c = epub.EpubHtml(title=chapternames[i], file_name=f'chap_{int(start) + i}-1.xhtml', lang='hr')
    chapters.append(c)
    book.add_item(c)
    toc.append(epub.Link(f'chap_{int(start) + i}.xhtml', chapternames[i], chapternames[i]))


    cstring = cstr[i]
    urls = []
    content = requests.get(chapter_prefix + cstring).content
    soup = bs4.BeautifulSoup(content, features='lxml')
    for img in soup.findAll('img'):
        url = img.get('src')
        if ("png" not in url.lower() and "wp-content" not in url.lower() and "credits" not in url.lower()):
            urls.append(url.strip().lstrip())

    page = 0

    if (ignore_first):
        urls = urls[1:]

    #print(urls)
    for url in urls:
        


        resp = requests.get(url)
        content = resp.content
        testimg = Image.open(io.BytesIO(content))
        size = testimg.size
        if size[0] > size[1]:
            width = size[0] // 2
            height = size[1]
            left = testimg.copy()
            right = testimg
            left = left.crop((0, 0, width - 1, height))
            right = right.crop((width, 0, size[0], height))

            b1 = io.BytesIO()
            b2 = io.BytesIO()

            right.save(b1, format="JPEG")
            left.save(b2, format="JPEG")

            f1 = f"{int(start) + i}-{page}-1.jpg"
            f2 = f"{int(start) + i}-{page}-2.jpg"

            p1 = epub.EpubImage()
            p1.file_name = f1
            p1.media_type = 'image/jpeg'
            p1.content = b1.getvalue()

            p2 = epub.EpubImage()
            p2.file_name = f2
            p2.media_type = 'image/jpeg'
            p2.content = b2.getvalue()

            if page != 0:
                c = epub.EpubHtml(title=f"{chapternames[i]}-{page + 1}-1", file_name=f'chap_{int(start) + i}-{page + 1}-1.xhtml', lang='hr')
                book.add_item(c)
            c.content = f'<img src="{f1}" />'
            book.spine.append(c)
            book.add_item(p1)

            page2 = epub.EpubHtml(title=f"{chapternames[i]}-{page + 1}-2", file_name=f'chap_{int(start) + i}-{page + 1}-2.xhtml', lang='hr')
            book.add_item(page2)
            page2.content = f'<img src="{f2}" />'
            book.spine.append(page2)
            book.add_item(p2)
            page += 1
            #print("Finished page " + str(page))
            continue

        filename = f"{int(start) + i}-{page}.jpg"
        ei = epub.EpubImage()
        ei.file_name = filename
        ei.media_type = 'image/jpeg'

        ei.content = resp.content
        if page != 0:
            c = epub.EpubHtml(title=f"{chapternames[i]}-{page + 1}", file_name=f'chap_{int(start) + i}-{page + 1}.xhtml', lang='hr')
            book.add_item(c)
        c.content = f'<img src="{filename}" />'

        
        book.add_item(ei)
        book.spine.append(c)
        page += 1
        #print("Finished page " + str(page))

    print(f"Finished chapter {int(start) + i}")
    i += 1
    

book.toc = tuple(toc)

book.add_item(epub.EpubNcx())
book.add_item(epub.EpubNav())

style = 'img {position: absolute; height: 100%}'
nav_css = epub.EpubItem(uid="style_nav", file_name="style/nav.css", media_type="text/css", content=style)

book.add_item(nav_css)


epub.write_epub(f'{name}.epub', book, {})
print("Finished")