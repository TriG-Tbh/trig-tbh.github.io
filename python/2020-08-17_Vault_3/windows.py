import tkinter
from PIL import Image, ImageTk
import pyotp
import qrcode
import settings

class BasicWindow:
    def __init__(self):
        self.master = tkinter.Tk()

        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)


    def quit(self, event):
        self.master.destroy()

class CreatePassword:
    def __init__(self):
        self.master = tkinter.Tk()

        self.use2fa = False

        self.master.title("Create Password")

        tkinter.Label(self.master, text="Enter a password: ").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Label(self.master, text="Confirm your password: ").grid(row=1)
        self.e2 = tkinter.Entry(self.master)
        self.e2.grid(row=1, column=1)

        self.use2facheck = tkinter.BooleanVar()

        self.password = ""
        self.confirmpw = ""

        self.confirmed = False

        tkinter.Label(self.master, text="Use 2FA? ").grid(row=2)
        self.e3 = tkinter.Checkbutton(self.master, variable=self.use2facheck, onvalue=True, offvalue=False)
        self.e3.grid(row=2, column=1)
        
        self.button = tkinter.Button(self.master, text="Enter", command=self.confirm)
        self.button.grid(row=3)

        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)
        self.master.bind("<Return>", self.confirm2)

        self.master.mainloop()

    def quit(self, event):
        self.master.destroy()

    def confirm2(self, event):
        self.confirm()

    def confirm(self):
        self.password = self.e1.get()
        self.confirmpw = self.e2.get()
        self.use2fa = self.use2facheck.get()

        if self.password == "" or self.confirmpw == "":
            self.confirmed = False
            return self.master.destroy()
        
        self.confirmed = (self.password == self.confirmpw)
        self.master.destroy()


class MfaWindow:
    def __init__(self, login=True, code=None):
        self.master = tkinter.Tk()

        if code is None:
            self.master.destroy()

        self.logged_in = False

        self.totp = pyotp.TOTP(code)

        if not login:
            self.master.title("Set Up 2FA")

            tkinter.Label(self.master, text="Scan this QR code with a 2FA-compatible app to get your 2FA code.\nDon't lose it!").grid(row=0)
            
            
            code = qrcode.make(self.totp.provisioning_uri()).resize((500, 500))
            code = ImageTk.PhotoImage(code)
            tkinter.Label(image=code).grid(row=1)

        tkinter.Label(self.master, text="2FA Code: ").grid(row=2)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=3)

        self.button = tkinter.Button(self.master, text="Enter", command=self.confirm)
        self.button.grid(row=4)
        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)
        self.master.bind("<Return>", self.confirm2)
        self.master.mainloop()

    def quit(self, event):
        self.master.destroy()


    def confirm2(self, event):
        self.confirm()

    def confirm(self):
        if self.e1.get() == "":
            return self.master.destroy()
        self.logged_in = (str(self.totp.now()) == self.e1.get())
        self.master.destroy()



class PasswordWindow:
    def __init__(self):
        
        self.password = ""
        self.master = tkinter.Tk()

        self.master.title("Password Input")

        tkinter.Label(self.master, text="Enter password: ").grid(row=0)
    
        self.e1 = tkinter.Entry(self.master, show="*")
        self.e1.grid(row=0, column=1)

        

        self.button = tkinter.Button(self.master, text="Enter", command=self.getpw)
        self.button.grid(row=1)

        self.master.bind("<Control-q>", self.quit)
        self.master.bind("<Control-w>", self.quit)
        self.master.bind("<Return>", self.getpw2)

        self.master.mainloop()


    def quit(self, event):
        self.master.destroy()

    def getpw2(self, event):
        self.getpw()

    def getpw(self):
        text = self.e1.get()
        if text == "":
            return self.master.destroy()
        self.password = text
        self.master.destroy()

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class CanvasImage(ttk.Frame):
    ''' Advanced zoom of the image '''

    def get_scale(self, image):
        width, height = image.size
        larger = max(width, height)
        ratio = settings.DEFAULT_DISPLAY_SIZE / larger
        return ratio

    def __init__(self, mainframe, title, image):
        ttk.Frame.__init__(self, master=mainframe)
        #self.master.title('Simple zoom with mouse wheel')
        # Vertical and horizontal scrollbars for canvas
        # Open image
        self.image = image
        self.title = title
        # Create canvas and put image on it
        self.canvas = tk.Canvas(self.master, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        # Make the canvas expandable
        self.master.rowconfigure(0, weight=1)
        self.master.columnconfigure(0, weight=1)
        # Bind events to the Canvas
        self.canvas.bind('<ButtonPress-1>', self.move_from)
        self.canvas.bind('<B1-Motion>',     self.move_to)
        self.canvas.bind('<MouseWheel>', self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = self.get_scale(self.image)
        self.imageid = None
        self.delta = settings.SCALE_DELTA
        width, height = self.image.size
        self.base_size = (width, height)
        self.master.geometry(f"{round(width * self.imscale)}x{round(height * self.imscale)}")
        
        minsize, maxsize = 5, 20
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        self.canvas.scan_mark(event.x, event.y)

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        self.canvas.scan_dragto(event.x, event.y, gain=1)

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if max(self.base_size) < settings.DEFAULT_DISPLAY_SIZE:
            return
        if event.num == 5 or event.delta == -120:
            scale        /= self.delta
            self.imscale /= self.delta
            if self.imscale < self.get_scale(self.image):
                scale = self.get_scale(self.image)
                self.imscale = self.get_scale(self.image)
        if event.num == 4 or event.delta == 120:
            scale        *= self.delta
            self.imscale *= self.delta
            if self.imscale > settings.SCALE_CAP:
                self.imscale = settings.SCALE_CAP
                scale = settings.SCALE_CAP
            
        # Rescale all canvas objects
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.canvas.scale('all', x, y, scale, scale)
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))

    def show_image(self):
        ''' Show image on the Canvas '''
        if self.imageid:
            self.canvas.delete(self.imageid)
            self.imageid = None
            self.canvas.imagetk = None  # delete previous image from the canvas
        width, height = self.image.size
        new_size = round(self.imscale * width), round(self.imscale * height)
        imagetk = ImageTk.PhotoImage(self.image.resize(new_size))
        # Use self.text object to set proper coordinates
        self.imageid = self.canvas.create_image(0, 0,
                                                anchor='nw', image=imagetk)
        self.master.title(self.title + " ({}x{})".format(*new_size))
        self.master.maxsize(*new_size)
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection
