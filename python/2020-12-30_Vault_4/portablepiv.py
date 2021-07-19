from PIL import Image, ImageTk, ImageGrab
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
#import praw
import re
import zlib
import base64
on_windows = False

try:
    import win32clipboard
except:
    on_windows = False
else:
    on_windows = True




class ImageViewer:
    def __init__(self, master, files):
        self.master = master
        self.images = {}
        self.imagepointer = 0

        self.canvas = tkinter.Canvas(self.master)
        self.canvas.grid(row=0)

        self.menubar = tkinter.Menu(self.master)

        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
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

        self.controlmenu.add_command(
            label="Save", command=lambda: self.save(self.imagepointer))
        self.controlmenu.entryconfig("Save", state="disabled")


        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)
        self.master.bind("<Control-s>", self.placeholder)
        if on_windows:
            self.master.bind("<Control-c>", self.placeholder)

        self.master.bind("<Left>", self.previous)
        self.master.bind("<Right>", self.next)

        self.master.config(menu=self.menubar)

        self.master.title("Private Image Viewer 2")
        
        cleared = False
        iterate = 0
        for name in files:
            iterate += 1
            base = os.path.dirname(os.path.realpath(__file__))
            path = os.path.join(os.path.join(os.path.join(base, "Journal"), "Images"), name)
            name, image = functions.get_image(path)
            if image is not None:
                if not cleared:
                    self.images = {}
                    cleared = True
                self.images["Attachment " + str(iterate)] = image
      
        if self.images != {}:
            self.images = {
                i: self.images[i]
                for i in self.natural_sort(list(self.images.keys()))
            }
            self.imagepointer = 0
            self.display(self.imagepointer)

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
                

    def copy(self, pointer):
        name = list(self.images.keys())[pointer]
        image = list(self.images.values())[pointer].convert("RGBA")
        output = io.BytesIO()
        image.save(output, "BMP")
        data = output.getvalue()[14:]
        self.send_to_clipboard(win32clipboard.CF_DIB, data)

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

        self.canvas = windows.CanvasImage(self.master,
                                           title=name,
                                           image=image)
        #self.canvas.__show_image()
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



