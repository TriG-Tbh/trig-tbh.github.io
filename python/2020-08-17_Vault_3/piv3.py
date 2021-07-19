# Image displaying modules
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PIL import Image, ImageGrab, ImageQt

# Operational modules
import sys
import tkinter
import requests
import io
import os
from tkinter import filedialog
import glob
import praw
import re
on_windows = False
try:
    import win32clipboard
except:
    on_windows = False
else:
    on_windows = True

# Other modules
import functions
import windows
import settings

reddit = praw.Reddit(client_id='[REDACTED]',
                     client_secret='[REDACTED]',
                     user_agent='[REDACTED]')

class RedditImagePuller:
    def __init__(self, master):
        self.master = master

        self.master.title("Get Images from Reddit")

        tkinter.Label(self.master, text="Subreddit: r/").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Label(self.master, text="Number of posts: ").grid(row=1)
        self.e2 = tkinter.Entry(self.master)
        self.e2.delete(0, "end")
        self.e2.insert(0, str(settings.POST_LIMIT))
        self.e2.grid(row=1, column=1)

        tkinter.Label(self.master, text="Sort: ").grid(row=2)
        self.sort = tkinter.StringVar(self.master)
        self.sort.set(settings.DEFAULT_SORT)
        self.e3 = tkinter.OptionMenu(self.master, self.sort, "Hot", "New", "Top", "Controversial")
        self.e3.grid(row=2, column=1)

        tkinter.Label(self.master, text="Allow NSFW Posts? ").grid(row=3)
        self.allow_nsfw = tkinter.BooleanVar()
        self.e4 = tkinter.Checkbutton(self.master, variable=self.allow_nsfw, offvalue=False, onvalue=True)
        self.e4.grid(row=3, column=1)

        tkinter.Label(self.master, text="Shuffle Posts? ").grid(row=4)
        self.shuffle_posts = tkinter.BooleanVar()
        self.e5 = tkinter.Checkbutton(self.master, variable=self.shuffle_posts, offvalue=False, onvalue=True)
        self.e5.grid(row=4, column=1)

        tkinter.Button(self.master, text="Get Posts", command=self.download_images).grid(row=5)

        self.images = {}

    def validate_sub(self, sub):
        try:
            reddit.subreddit(sub)
        except:
            return False
        return True

    def download_images(self, event=None):
        sub = self.e1.get()
        if not self.validate_sub(sub):
            self.master.quit()
            return self.master.destroy()
        subreddit = reddit.subreddit(sub)
        limit = self.e2.get()
        try:
            limit = int(limit)
        except:
            return self.master.destroy()
        sorts = {
            "Hot": subreddit.hot(limit=(limit*2)),
            "New": subreddit.new(limit=(limit*2)),
            "Top": subreddit.top(limit=(limit*2)),
            "Controversial": subreddit.controversial(limit=(limit*2))
        }
        sort = sorts[self.sort.get()]
        allow_nsfw = self.allow_nsfw.get()
        shuffle = self.shuffle_posts.get()

        i = 0
        for post in sort:
            if i >= limit:
                break
            if not post.is_self:
                if not post.over_18 or (post.over_18 == allow_nsfw):
                    _, image = functions.get_image(post.url)
                    name = post.title
                    if image is None:
                        continue
                    self.images[name] = image
                    i += 1
        self.master.quit()
        return self.master.destroy()

    def run(self):
        self.master.mainloop()

class URLGrabber:
    def __init__(self, master):
        self.master = master

        self.images = {}

        self.master.title("Get Image")

        tkinter.Label(self.master, text="Image URL: ").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Button(self.master, text="Get Image", command=self.download_image).grid(row=1)

    def download_image(self, event=None):
        url = self.e1.get()
        name, image = functions.get_image(url)
        if image is None:
            self.master.quit()
            return self.master.destroy()
        self.images = {name: image}
        self.master.quit()
        return self.master.destroy()

    def run(self):
        self.master.mainloop()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.images = {}
        self.imagepointer = 0

        self.setGeometry(0, 0, 300, 300)
        self.setWindowTitle("Private Image Viewer 3")
        self.show()

    def placeholder(self, event=None):
        pass # Placeholder used for disabled keyboard shortcuts

    def send_to_clipboard(self, clip_type, data):
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardData(clip_type, data)
        win32clipboard.CloseClipboard()

    def open_reddit(self):
        imagepuller = RedditImagePuller(tkinter.Toplevel())
        imagepuller.run()
        if imagepuller.images != {}:
            
            self.images = imagepuller.images
            self.imagepointer = 0
            self.display(0)

    def open_url(self):
        urlgrabber = URLGrabber(tkinter.Tk())
        urlgrabber.run()
        if urlgrabber.images != {}:
            self.images = urlgrabber.images
            self.imagepointer = 0
            self.display(0)

    def open_image(self):
        file = filedialog.askopenfilename()
        if file is None:
            return
        name, image = functions.get_image(file)
        if image is None:
            return

        self.images = {name: image}
        self.imagepointer = 0
        self.display(self.imagepointer)

    def natural_sort(self, l):
        convert = lambda text: int(text) if text.isdigit() else text.lower() 
        alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)] 
        return sorted(l, key=alphanum_key)

    def open_folder(self):
        folder = filedialog.askdirectory()
        if folder is None:
            return
        if os.path.isdir(folder):
            cleared = False
            os.chdir(folder)
            for filename in glob.glob("*"):
                path = os.path.join(folder, filename)
                name, image = functions.get_image(path)
                if image is not None:
                    if not cleared:
                        self.images = {}
                        cleared = True
                    self.images[name] = image
        else:
            return
        if self.images != {}:
            self.images = {i: self.images[i] for i in self.natural_sort(list(self.images.keys()))}
            self.imagepointer = 0
            self.display(self.imagepointer)

    def next(self, event=None):
        if settings.WRAP_AROUND:
            if self.imagepointer == len(self.images) - 1:
                self.imagepointer = 0
            else:
                self.imagepointer = self.imagepointer + 1
        elif self.imagepointer < len(self.images) - 1:
            self.imagepointer += 1
        self.display(self.imagepointer)

    def previous(self, event=None):
        if settings.WRAP_AROUND:
            if self.imagepointer > 0:
                self.imagepointer = self.imagepointer - 1
            else:
                self.imagepointer = len(self.images) - 1
        elif self.imagepointer > 0:
            self.imagepointer -= 1
        self.display(self.imagepointer)

    def display(self, pointer):
        if len(self.images) == 0:
            return
        image = list(self.images.values())[pointer]
        name = list(self.images.keys())[pointer]
        name = "".join([name[j] for j in range(len(name)) if ord(name[j]) in range(65536)])

    def save(self, pointer):
        filetypes = [("Encrypted File", ".enc"), ("PNG File", ".png")]
        path = os.path.dirname(os.path.realpath(__file__))
        savepath = filedialog.asksaveasfilename(parent=self.master,
                                      initialdir=path,
                                      filetypes=filetypes)
        if savepath == "":
            return
        name = list(self.images.keys())[pointer]
        image = list(self.images.values())[pointer].convert("RGBA")
        buffer = io.BytesIO()
        extension = ".".join(name.split(".")[1:])
        image.save(buffer, format="png")
        bytedata = buffer.getvalue()
        if savepath.endswith(".enc"):
            bytedata = functions.fernet.encrypt(bytedata)
            
            with open(savepath, "wb") as f:
                f.write(bytedata)
            
            with open(savepath, "a") as f:
                extension = "." + ".".join(name.split(".")[1:])
                f.write("|" + extension)

            with open(savepath, "rb") as f:
                encrypted_bytes = f.read()
            double_encrypted = functions.fernet.encrypt(encrypted_bytes)
            with open(savepath, "wb") as f:
                f.write(double_encrypted)
        else:
            with open(savepath, "wb") as f:
                f.write(bytedata)

def main():
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()