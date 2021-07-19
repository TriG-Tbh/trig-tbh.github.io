from PIL import Image, ImageTk, ImageChops
import tkinter
import functions
import sys
import requests
import io
import os
from tkinter import filedialog
import windows
import glob
import settings
import praw
import re
#import windows2
import zlib
import base64
on_windows = False

try:
    import win32clipboard
except:
    on_windows = False
else:
    on_windows = True

if on_windows:
    from PIL import ImageGrab

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
        self.e3 = tkinter.OptionMenu(self.master, self.sort, "Hot", "New",
                                     "Top", "Controversial")
        self.e3.grid(row=2, column=1)

        self.l5 = tkinter.Label(self.master, text="Allow NSFW Posts? ")
        self.l5.grid(row=3)
        self.allow_nsfw = tkinter.BooleanVar()
        self.e5 = tkinter.Checkbutton(self.master,
                                      variable=self.allow_nsfw,
                                      offvalue=False,
                                      onvalue=True)
        self.e5.grid(row=3, column=1)

        self.l6 = tkinter.Label(self.master, text="Shuffle Posts? ")
        self.l6.grid(row=4)
        self.shuffle_posts = tkinter.BooleanVar()
        self.e6 = tkinter.Checkbutton(self.master,
                                      variable=self.shuffle_posts,
                                      offvalue=False,
                                      onvalue=True)
        self.e6.grid(row=4, column=1)

        self.gobutton = tkinter.Button(self.master,
                                       text="Get Posts",
                                       command=self.download_images)
        self.gobutton.grid(row=5)

        #self.master.bind("<Enter>", self.download_images)
        self.l4 = None
        self.e4 = None
        self.limit = None

        self.images = {}

    def onsortwrite(self, *args):
        sort = self.sort.get()
        if sort == "Top" or sort == "Controversial":
            self.l4 = tkinter.Label(self.master, text="Time span: ")
            self.limit = tkinter.StringVar(self.master)
            self.limit.set(settings.DEFAULT_LIMIT)
            self.e4 = tkinter.OptionMenu(self.master, self.limit, "Past Day",
                                         "Past Week", "Past Month",
                                         "Past Year", "All Time")

            self.l4.grid(row=3)
            self.e4.grid(row=3, column=1)
            self.l5.grid(row=4)
            self.e5.grid(row=4, column=1)
            self.l6.grid(row=5)
            self.e6.grid(row=5, column=1)
            self.gobutton.grid(row=6)

        else:
            if self.l4 is not None:
                self.l4.grid_forget()
                self.e4.grid_forget()
                self.l4 = None
                self.e4 = None
                self.limit = None
            self.l5.grid(row=3)
            self.e5.grid(row=3, column=1)
            self.l6.grid(row=4)
            self.e6.grid(row=4, column=1)
            self.gobutton.grid(row=5)
            for label in self.master.grid_slaves():
                if int(label.grid_info()["row"]) == 6:
                    label.grid_forget()

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
            "Hot": subreddit.hot(limit=(limit * 2)),
            "New": subreddit.new(limit=(limit * 2)),
        }

        sorttype = self.sort.get()

        if sorttype == "Top" or sorttype == "Controversial":
            durations = {
                "Past Day": "day",
                "Past Week": "week",
                "Past Month": "month",
                "Past Year": "year",
                "All Time": "all"
            }
            sorts["Top"] = subreddit.top(durations[self.limit.get()],
                                         limit=(limit * 2))
            sorts["Controversial"] = subreddit.controversial(
                durations[self.limit.get()], limit=(limit * 2))

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
        self.sort.trace("w", self.onsortwrite)
        self.master.mainloop()


class URLGrabber:
    def __init__(self, master):
        self.master = master

        self.images = {}

        self.master.title("Get Image")

        tkinter.Label(self.master, text="Image URL: ").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Button(self.master,
                       text="Get Image",
                       command=self.download_image).grid(row=1)

        #self.master.bind("<Enter>", self.download_image)

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


class ImageViewer:
    def __init__(self, master):
        self.master = master
        self.images = {}
        self.imagepointer = 0

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.grid(row=0)

        self.menubar = tkinter.Menu(self.master)

        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open Image", command=self.open_image)
        self.filemenu.add_command(label="Open Folder",
                                  command=self.open_folder)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)

        self.controlmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Control", menu=self.controlmenu)
        self.controlmenu.add_command(label="Next", command=self.next)
        self.controlmenu.add_command(label="Previous", command=self.previous)

        self.controlmenu.entryconfig("Next", state="disabled")
        self.controlmenu.entryconfig("Previous", state="disabled")

        if on_windows:
            self.controlmenu.add_command(
                label="Copy", command=lambda: self.copy(self.imagepointer))
            self.controlmenu.entryconfig("Copy", state="disabled")

        self.controlmenu.add_command(label="Paste",
                                     command=lambda: self.paste())
        self.master.bind("<Control-v>", lambda event: self.paste())
        self.controlmenu.add_command(
            label="Save", command=lambda: self.save(self.imagepointer))
        self.controlmenu.entryconfig("Save", state="disabled")

        self.imenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Internet", menu=self.imenu)
        self.imenu.add_command(label="Get Reddit Images",
                               command=self.open_reddit)
        self.imenu.add_command(label="Open Image URL", command=self.open_url)

        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)
        self.master.bind("<Control-s>", self.placeholder)
        if on_windows:
            self.master.bind("<Control-c>", self.placeholder)

        self.master.bind("<Left>", self.previous)
        self.master.bind("<Right>", self.next)

        self.master.config(menu=self.menubar)

        self.master.title("Private Image Viewer 2")

    def placeholder(self, event=None):
        pass  # Placeholder used for disabled keyboard shortcuts

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
        """with open(file, "rb") as f:
            b = f.read()
        b = functions.fernet.decrypt(b)
        blank = Image.open(io.BytesIO(b))
        self.images = {file: blank}
        self.imagepointer = 0
        return self.display(self.imagepointer)"""
        name, image = functions.get_image(file)
        if image is None:
            return

        self.images = {name: image}
        self.imagepointer = 0
        self.display(self.imagepointer)

    def natural_sort(self, l):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [
            convert(c) for c in re.split('([0-9]+)', key)
        ]
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
                #print(filename)
                name, image = functions.get_image(path)
                if image is not None:
                    if not cleared:
                        self.images = {}
                        cleared = True
                    self.images[name] = image
        else:
            return
        if self.images != {}:
            self.images = {
                i: self.images[i]
                for i in self.natural_sort(list(self.images.keys()))
            }
            self.imagepointer = 0
            self.display(self.imagepointer)

    def copy(self, pointer):
        name = list(self.images.keys())[pointer]
        image = list(self.images.values())[pointer].convert("RGBA")
        output = io.BytesIO()
        image.save(output, "BMP")
        data = output.getvalue()[14:]
        self.send_to_clipboard(win32clipboard.CF_DIB, data)

    def paste(self):
        image = ImageGrab.grabclipboard()
        if image is None:
            return
        image = image.convert("RGBA")
        self.images = {"unknown.png": image}
        self.imagepointer = 0
        self.display(self.imagepointer)

    def display(self, pointer):
        if len(self.images) == 0:
            return
        image = list(self.images.values())[pointer]
        name = list(self.images.keys())[pointer]
        name = "".join([
            name[j] for j in range(len(name)) if ord(name[j]) in range(65536)
        ])
        self.master.title(name)
        if len(self.images) == 1:
            self.controlmenu.entryconfig("Next", state="disabled")
            self.controlmenu.entryconfig("Previous", state="disabled")
        else:

            if pointer == 0:
                if not settings.WRAP_AROUND:
                    self.controlmenu.entryconfig("Previous", state="disabled")
            else:
                self.controlmenu.entryconfig("Previous", state="normal")
            if pointer == len(self.images) - 1:
                if not settings.WRAP_AROUND:
                    self.controlmenu.entryconfig("Next", state="disabled")
            else:
                self.controlmenu.entryconfig("Next", state="normal")

        if on_windows:
            self.controlmenu.entryconfig("Copy", state="normal")
            self.master.bind("<Control-c>",
                             lambda event: self.copy(self.imagepointer))

        self.controlmenu.entryconfig("Save", state="normal")
        self.master.bind("<Control-s>",
                         lambda event: self.save(self.imagepointer))

        self.master.bind("<space>",
                         lambda event: self.display(self.imagepointer))

        self.canvas.destroy()
        self.canvas = windows.CanvasImage2(self.master,
                                           title=name,
                                           image=ImageChops.duplicate(image))
        self.canvas.grid(row=0, column=0)

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
        #image.save(savepath)
        buffer = io.BytesIO()
        extension = ".".join(name.split(".")[1:])
        image.save(buffer, format="png")
        bytedata = buffer.getvalue()
        if savepath.endswith(".enc"):
            bytedata = functions.fernet.encrypt(bytedata)
            """with open(savepath, "wb") as f:
                return f.write(bytedata)"""
            
            extension = "|." + ".".join(name.split(".")[1:])
            if extension == "|.":
                extension = "|.png"
            data = bytedata + bytes(extension, encoding="utf-8")

            
            double_encrypted = functions.fernet.encrypt(data)
            with open(savepath, "wb") as f:
                compressed = base64.b64encode(zlib.compress(double_encrypted))
                #print(zlib.compress(double_encrypted)[:15])
                #print(compressed[:15])
                f.write(compressed)

        else:
            with open(savepath, "wb") as f:
                f.write(bytedata)

    def quit(self, event):
        self.master.destroy()

    def run(self):
        self.master.mainloop()


#functions.create_new_password(generate_key=True)

if __name__ == "__main__":
    """if on_windows:
        if not functions.login():
            sys.exit(0)"""
    functions.key_login(key="[REDACTED]")
    master = tkinter.Tk()
    viewer = ImageViewer(master)
    viewer.run()
