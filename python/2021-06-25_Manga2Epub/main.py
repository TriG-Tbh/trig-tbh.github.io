from ebooklib import epub
import bs4, requests

book = epub.EpubBook()

name = input("Name of book: ")

book.set_title(name)
book.set_language('en')
book.set_direction("rtl")

author = input("Author name: ")

book.add_author(author)

start = input("Start chapter (inclusive): ")
end = input("End chapter (inclusive): ")
chapter_prefix = input("Chapter URL prefix: ")
cover_art = input("Cover art: ")



ignore_first = (True if input("Remove first page of every chapter? ") != "" else False)

chapternames = [f"Chapter {int(start) + i}" for i in range(int(end) - int(start) + 1)]

chapters = []
toc = []

ei = epub.EpubImage()
ei.file_name = "cover.jpeg"
ei.media_type = 'image/jpeg'
resp = requests.get(cover_art)
ei.content = resp.content
#book.add_item(ei)
book.set_cover("EPUB/cover.jpeg", resp.content)


#print(book.spine)


cstr = [str(c) for c in range(int(start), int(end) + 1)]

"""
ccount = 0
for cstring in cstr:
    
    urls = []
    content = requests.get(chapter_prefix + cstring).content
    soup = bs4.BeautifulSoup(content, features='lxml')
    for img in soup.findAll('img'):
        url = img.get('src')
        if ("png" not in url.lower() and "wp-content" not in url.lower() and "credits" not in url.lower()):
            urls.append(url.strip().lstrip())


    c = chapters[ccount]
    c.content = ""

    ucount = 1
    for u in urls:
        if ucount == 1 and ignore_first:
            ucount += 1            
            continue
        filename = f"{int(start) + ccount}-{ucount}.jpg"
        c.content = c.content + f'<div><img src="{int(start) + ccount}-{ucount}.jpg" /></div>'
        
        ei = epub.EpubImage()
        ei.file_name = filename
        ei.media_type = 'image/jpeg'

        resp = requests.get(u)
        ei.content = resp.content
        book.add_item(ei)
        
        #print(f"Finished page {ucount}")
        ucount += 1
    print(f"Finished chapter {int(start) + ccount}")
    ccount += 1
"""
book.spine = []

cstr = [str(c) for c in range(int(start), int(end) + 1)]
i = 0
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
    for url in urls:
        if url == urls[0] and ignore_first:
            continue
        filename = f"{int(start) + i}-{page}.jpg"
        if page != 0:
            c = epub.EpubHtml(title=f"{chapternames[i]}-{page + 1}", file_name=f'chap_{int(start) + i}-{page + 1}.xhtml', lang='hr')
            book.add_item(c)
        c.content = f'<img src="{filename}" />'

        ei = epub.EpubImage()
        ei.file_name = filename
        ei.media_type = 'image/jpeg'

        resp = requests.get(url)
        ei.content = resp.content
        book.add_item(ei)
        book.spine.append(c)
        page += 1

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