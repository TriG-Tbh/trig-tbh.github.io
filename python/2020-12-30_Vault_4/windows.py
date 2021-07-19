import tkinter
from PIL import Image, ImageTk
#import pyotp
#import qrcode
import settings
import math
import warnings
import tkinter as tk

from tkinter import ttk
from PIL import Image, ImageTk


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
        self.e3 = tkinter.Checkbutton(self.master,
                                      variable=self.use2facheck,
                                      onvalue=True,
                                      offvalue=False)
        self.e3.grid(row=2, column=1)

        self.button = tkinter.Button(self.master,
                                     text="Enter",
                                     command=self.confirm)
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

            tkinter.Label(
                self.master,
                text=
                "Scan this QR code with a 2FA-compatible app to get your 2FA code.\nDon't lose it!"
            ).grid(row=0)

            code = qrcode.make(self.totp.provisioning_uri()).resize((500, 500))
            code = ImageTk.PhotoImage(code)
            tkinter.Label(image=code).grid(row=1)

        tkinter.Label(self.master, text="2FA Code: ").grid(row=2)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=3)

        self.button = tkinter.Button(self.master,
                                     text="Enter",
                                     command=self.confirm)
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

        self.button = tkinter.Button(self.master,
                                     text="Enter",
                                     command=self.getpw)
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
        self.canvas.bind("<ButtonRelease-1>", self.store_topleft)
        self.canvas.bind('<B1-Motion>', self.move_to)
        self.canvas.bind('<MouseWheel>',
                         self.wheel)  # with Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',
                         self.wheel)  # only with Linux, wheel scroll down
        self.canvas.bind('<Button-4>',
                         self.wheel)  # only with Linux, wheel scroll up
        # Show image and plot some random test rectangles on the canvas
        self.imscale = self.get_scale(self.image)
        
        self.imageid = None

        self.delta = settings.SCALE_DELTA
        width, height = self.image.size
        self.base_size = (width, height)
        self.master.geometry(
            f"{round(width * self.imscale)}x{round(height * self.imscale)}")

        
        self.imcopy = self.image
        width, height = self.imcopy.size
        self.new_size = round(self.imscale * width), round(self.imscale * height)
        self.sizecopy = self.new_size
        self.image = self.imcopy.resize(self.new_size)
        self.topleft = (0, 0)
        self.tlcopy = self.topleft
        self.basex = 0
        self.basey = 0
        self.show_image()
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))
        

    def move_from(self, event):
        ''' Remember previous coordinates for scrolling with the mouse '''
        #self.canvas.scan_mark(event.x, event.y)
        self.basex = event.x
        self.basey = event.y

    def move_to(self, event):
        ''' Drag (move) canvas to the new position '''
        dx = -(event.x - self.basex)
        dy = -(event.y - self.basey)
        
        #print(dx, dy)
        """if self.topleft[0] + dx + self.base_size[0] > self.image.size[0]:
            dx = self.image.size[0] - self.base_size[0]
        if self.topleft[0] + dx < 0:
            dx = -self.topleft[0]

        if self.topleft[1] + dy + self.base_size[1] > self.image.size[1]:
            dy = self.image.size[1] - self.base_size[1]
        if self.topleft[1] + dy < 0:
            dy = -self.topleft[1]"""

        #print(dx, dy)
        self.tlcopy = (self.topleft[0] + dx, self.topleft[1] + dy)
        #print(self.tlcopy)
        self.show_image()
        #self.canvas.scan_dragto(event.x, event.y, gain=1)
    
    def store_topleft(self, event):
        self.topleft = self.tlcopy

    def wheel(self, event):
        ''' Zoom with mouse wheel '''
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if max(self.base_size) < settings.DEFAULT_DISPLAY_SIZE:
            return
        
        if event.num == 5 or event.delta == -120:
            #print(1)
            if self.imscale == self.get_scale(self.imcopy):
                return
            scale /= self.delta
            self.imscale /= self.delta
            if self.imscale < self.get_scale(self.imcopy):
                scale = self.get_scale(self.imcopy)
                self.imscale = self.get_scale(self.imcopy)
        if event.num == 4 or event.delta == 120:
            #print(2)
            if self.imscale == settings.SCALE_CAP:
                return
            scale *= self.delta
            self.imscale *= self.delta
            if self.imscale > settings.SCALE_CAP:
                self.imscale = settings.SCALE_CAP
                scale = settings.SCALE_CAP

        # Rescale all canvas objects
        width, height = self.imcopy.size
        self.new_size = round(self.imscale * width), round(self.imscale * height)

        posx = event.x + self.tlcopy[0]
        posy = event.y + self.tlcopy[1]

        rx = posx / self.image.size[0]
        ry = posy / self.image.size[1]

        #print(rx, ry)

        #print(posx, posy)
        self.image = self.imcopy.resize(self.new_size)

        equivalent = (self.new_size[0] * rx, self.new_size[1] * ry)
        #print(equivalent)

        self.tlcopy = ((equivalent[0] - (self.sizecopy[0] / 2)) / 1, (equivalent[1] - (self.sizecopy[1] / 2)) / 1)
        self.topleft = self.tlcopy
        #self.tlcopy = (posx / self.imscale, posy / self.imscale)
        #self.tlcopy = (100, 100)
        
        
        #self.tlcopy = (posx + self.base_size[0] / 2, posy + self.base_size[1] / 2)

        
        #print(posx, posy)


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
        

        if self.tlcopy[0] < 0:
            self.tlcopy = (0, self.tlcopy[1])
        if self.tlcopy[1] < 0:
            self.tlcopy = (self.tlcopy[0], 0)
        
        if self.tlcopy[0] + self.sizecopy[0] > self.image.size[0]:
            self.tlcopy = (self.image.size[0] - self.sizecopy[0], self.tlcopy[1])
        
        if self.tlcopy[1] + self.sizecopy[1] > self.image.size[1]:
            self.tlcopy = (self.tlcopy[0], self.image.size[1] - self.sizecopy[1])
        
        # Use self.text object to set proper coordinates
        #print(self.canvas.x)
        #print((self.tlcopy[0], self.tlcopy[1], self.tlcopy[0] + self.base_size[0], self.tlcopy[1] + self.base_size[1]))
        imagetk = ImageTk.PhotoImage(self.image.crop((self.tlcopy[0], self.tlcopy[1], self.tlcopy[0] + self.base_size[0], self.tlcopy[1] + self.base_size[1])))
        #self.canvas.xview("scroll", -50, "unit")
        #self.canvas.yview("scroll", -50, "unit")
        self.imageid = self.canvas.create_image(0, 0, 
                                                anchor='nw',
                                                image=imagetk)
        self.master.title(self.title + " ({}x{})".format(*self.new_size))
        self.canvas.lower(self.imageid)  # set it into background
        self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection











class AutoScrollbar(ttk.Scrollbar):
    """ A scrollbar that hides itself if it's not needed. Works only for grid geometry manager """
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            #self.grid()
            ttk.Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise tk.TclError('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        raise tk.TclError('Cannot use place with the widget ' + self.__class__.__name__)

class CanvasImage2:
    def get_scale(self, image):
        width, height = image.size
        larger = max(width, height)
        ratio = settings.DEFAULT_DISPLAY_SIZE / larger
        return ratio

    def __init__(self, placeholder, image, title):
        """ Initialize the ImageFrame """

        self.title = title
        self.imcopy = image
        self.placeholder = placeholder

        self.zoom_out = False
        self.imscale = self.get_scale(image)  # scale for the canvas image zoom, public for outer classes
        self.__delta = settings.SCALE_DELTA  # zoom magnitude
        self.__filter = Image.ANTIALIAS  # could be: NEAREST, BILINEAR, BICUBIC and ANTIALIAS
        self.__previous_state = 0  # previous state of the keyboard
        self.baseimage = image  # path to the image, should be public for outer classes
        # Create ImageFrame in placeholder widget
        
        self.drawcopy = (0, 0)
        self.boxcopy = []
        size = image.size
        self.init_x = round(size[0] * self.get_scale(image))
        self.init_y = round(size[1] * self.get_scale(image))
        
        placeholder.geometry("{}x{}".format(self.init_x, self.init_y))

        self.__imframe = ttk.Frame(placeholder, width=self.init_x, height=self.init_y)  # placeholder of the ImageFrame object

        # Vertical and horizontal scrollbars for canvas
        hbar = AutoScrollbar(self.__imframe, orient='horizontal')
        vbar = AutoScrollbar(self.__imframe, orient='vertical')
        hbar.grid(row=1, column=0, sticky='we')
        vbar.grid(row=0, column=1, sticky='ns')
        # Create canvas and bind it with scrollbars. Public for outer classes
        self.canvas = tk.Canvas(self.__imframe, highlightthickness=0,
                                xscrollcommand=hbar.set, yscrollcommand=vbar.set, width=self.init_x, height=self.init_y)
        self.canvas.grid(row=0, column=0, sticky='nswe')
        self.canvas.update()  # wait till canvas is created
        hbar.configure(command=self.__scroll_x)  # bind scrollbars to the canvas
        vbar.configure(command=self.__scroll_y)
        # Bind events to the Canvas
        self.canvas.bind('<Configure>', lambda event: self.__show_image())  # canvas is resized
        self.canvas.bind('<ButtonPress-1>', self.__move_from)  # remember canvas position
        self.canvas.bind('<B1-Motion>',     self.__move_to)  # move canvas to the new position
        self.canvas.bind('<MouseWheel>', self.__wheel)  # zoom for Windows and MacOS, but not Linux
        self.canvas.bind('<Button-5>',   self.__wheel)  # zoom for Linux, wheel scroll down
        self.canvas.bind('<Button-4>',   self.__wheel)  # zoom for Linux, wheel scroll up
        # Handle keystrokes in idle mode, because program slows down on a weak computers,
        # when too many key stroke events in the same time
        self.canvas.bind('<Key>', lambda event: self.canvas.after_idle(self.__keystroke, event))
        # Decide if this image huge or not
        self.__huge = False  # huge or not
        self.__huge_size = 14000  # define size of the huge image
        self.__band_width = 1024  # width of the tile band
        Image.MAX_IMAGE_PIXELS = 1000000000  # suppress DecompressionBombError for the big image
        with warnings.catch_warnings():  # suppress DecompressionBombWarning
            warnings.simplefilter('ignore')
            self.__image = self.baseimage  # open image, but down't load it
        self.imwidth, self.imheight = self.__image.size  # public for outer classes
        if self.imwidth * self.imheight > self.__huge_size * self.__huge_size and \
           self.__image.tile[0][0] == 'raw':  # only raw images could be tiled
            self.__huge = True  # image is huge
            self.__offset = self.__image.tile[0][2]  # initial tile offset
            self.__tile = [self.__image.tile[0][0],  # it have to be 'raw'
                           [0, 0, self.imwidth, 0],  # tile extent (a rectangle)
                           self.__offset,
                           self.__image.tile[0][3]]  # list of arguments to the decoder
        self.__min_side = min(self.imwidth, self.imheight)  # get the smaller image side
        # Create image pyramid
        self.__pyramid = [self.smaller()] if self.__huge else [self.baseimage]
        # Set ratio coefficient for image pyramid
        self.__ratio = max(self.imwidth, self.imheight) / self.__huge_size if self.__huge else 1.0
        self.__curr_img = 0  # current image from the pyramid
        self.__scale = self.imscale * self.__ratio  # image pyramide scale
        self.__reduction = 2  # reduction degree of image pyramid
        w, h = self.__pyramid[-1].size
        while w > 512 and h > 512:  # top pyramid image is around 512 pixels in size
            w /= self.__reduction  # divide on reduction degree
            h /= self.__reduction  # divide on reduction degree
            self.__pyramid.append(self.__pyramid[-1].resize((int(w), int(h)), self.__filter))
        # Put image into container rectangle and use it to set proper coordinates to the image
        self.container = self.canvas.create_rectangle((0, 0, self.imwidth, self.imheight), width=0)
        self.__show_image()  # show image on the canvas
        self.canvas.focus_set()  # set focus on the canvas

    def smaller(self):
        """ Resize image proportionally and return smaller image """
        w1, h1 = float(self.imwidth), float(self.imheight)
        w2, h2 = float(self.__huge_size), float(self.__huge_size)
        aspect_ratio1 = w1 / h1
        aspect_ratio2 = w2 / h2  # it equals to 1.0
        if aspect_ratio1 == aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(w2)  # band length
        elif aspect_ratio1 > aspect_ratio2:
            image = Image.new('RGB', (int(w2), int(w2 / aspect_ratio1)))
            k = h2 / w1  # compression ratio
            w = int(w2)  # band length
        else:  # aspect_ratio1 < aspect_ration2
            image = Image.new('RGB', (int(h2 * aspect_ratio1), int(h2)))
            k = h2 / h1  # compression ratio
            w = int(h2 * aspect_ratio1)  # band length
        i, j, n = 0, 1, round(0.5 + self.imheight / self.__band_width)
        while i < self.imheight:
            band = min(self.__band_width, self.imheight - i)  # width of the tile band
            self.__tile[1][3] = band  # set band width
            self.__tile[2] = self.__offset + self.imwidth * i * 3  # tile offset (3 bytes per pixel)
            self.__image.close()
            self.__image = self.baseimage  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]  # set tile
            cropped = self.__image.crop((0, 0, self.imwidth, band))  # crop tile band
            image.paste(cropped.resize((w, int(band * k)+1), self.__filter), (0, int(i * k)))
            i += band
            j += 1
        return image

    def redraw_figures(self):
        """ Dummy function to redraw figures in the children classes """
        pass

    def grid(self, **kw):
        """ Put CanvasImage widget on the parent widget """
        self.__imframe.grid(**kw)  # place CanvasImage widget on the grid
        self.__imframe.grid(sticky='nswe')  # make frame container sticky
        self.__imframe.rowconfigure(0, weight=1)  # make canvas expandable
        self.__imframe.columnconfigure(0, weight=1)

    def pack(self, **kw):
        """ Exception: cannot use pack with this widget """
        raise Exception('Cannot use pack with the widget ' + self.__class__.__name__)

    def place(self, **kw):
        """ Exception: cannot use place with this widget """
        raise Exception('Cannot use place with the widget ' + self.__class__.__name__)

    # noinspection PyUnusedLocal
    def __scroll_x(self, *args, **kwargs):
        """ Scroll canvas horizontally and redraw the image """
        self.canvas.xview(*args)  # scroll horizontally
        self.__show_image()  # redraw the image

    # noinspection PyUnusedLocal
    def __scroll_y(self, *args, **kwargs):
        """ Scroll canvas vertically and redraw the image """
        self.canvas.yview(*args)  # scroll vertically
        self.__show_image()  # redraw the image

    def __show_image(self):
        """ Show image on the Canvas. Implements correct image zoom almost like in Google Maps """
        box_image = self.canvas.coords(self.container)  # get image area
        box_canvas = (self.canvas.canvasx(0),  # get visible area of the canvas
                      self.canvas.canvasy(0),
                      self.canvas.canvasx(self.canvas.winfo_width()),
                      self.canvas.canvasy(self.canvas.winfo_height()))
        box_img_int = tuple(map(round, box_image))  # convert to integer or it will not work properly
        # Get scroll region box
        box_scroll = [min(box_img_int[0], box_canvas[0]), min(box_img_int[1], box_canvas[1]),
                      max(box_img_int[2], box_canvas[2]), max(box_img_int[3], box_canvas[3])]
        # Horizontal part of the image is in the visible area
        if  box_scroll[0] == box_canvas[0] and box_scroll[2] == box_canvas[2]:
            box_scroll[0]  = box_img_int[0]
            box_scroll[2]  = box_img_int[2]
        # Vertical part of the image is in the visible area
        if  box_scroll[1] == box_canvas[1] and box_scroll[3] == box_canvas[3]:
            box_scroll[1]  = box_img_int[1]
            box_scroll[3]  = box_img_int[3]

        box_scroll = list(map(int, box_scroll))
        box_scroll[2] = box_scroll[0] + round(self.baseimage.size[0] * self.imscale)
        box_scroll[3] = box_scroll[1] + round(self.baseimage.size[1] * self.imscale)
        
        difx = round(self.baseimage.size[0] * self.get_scale(self.baseimage))
        dify = round(self.baseimage.size[1] * self.get_scale(self.baseimage))
        # Convert scroll region to tuple and to integer
        self.canvas.configure(scrollregion=tuple(map(round, box_scroll)))  # set scroll region
        x1 = max(box_canvas[0] - box_image[0], 0)  # get coordinates (x1,y1,x2,y2) of the image tile
        y1 = max(box_canvas[1] - box_image[1], 0)
        x2 = x1 + difx
        y2 = y1 + dify
        if int(x2 - x1) > 0 and int(y2 - y1) > 0:  # show image if it in the visible area
            if self.__huge and self.__curr_img < 0:  # show huge image
                h = int((y2 - y1) / self.imscale)  # height of the tile band
                self.__tile[1][3] = h  # set the tile band height
                self.__tile[2] = self.__offset + self.imwidth * int(y1 / self.imscale) * 3
                self.__image.close()
                self.__image = self.baseimage  # reopen / reset image
                self.__image.size = (self.imwidth, h)  # set size of the tile band
                self.__image.tile = [self.__tile]
                image = self.__image.crop((int(x1 / self.imscale), 0, int(x2 / self.imscale), h))
            else:  # show normal image
                image = self.__pyramid[max(0, self.__curr_img)].crop(  # crop current img from pyramid
                                    (int(x1 / self.__scale), int(y1 / self.__scale),
                                     int(x2 / self.__scale), int(y2 / self.__scale)))
            #
            imagetk = ImageTk.PhotoImage(image.resize((round(x2 - x1), round(y2 - y1)), self.__filter))
            imageid = self.canvas.create_image(max(box_canvas[0], box_img_int[0]),
                                               max(box_canvas[1], box_img_int[1]),
                                               anchor='nw', image=imagetk)
            size = self.imcopy.size
            scl = self.get_scale(self.imcopy)
            self.placeholder.title(self.title + " ({}x{}, {}%)".format(round(size[0] * self.imscale), round(size[1] * self.imscale), round(size[0] * self.imscale / self.imcopy.size[0] * 100)))
            self.canvas.lower(imageid)  # set image into background
            self.canvas.imagetk = imagetk  # keep an extra reference to prevent garbage-collection

    def __move_from(self, event):
        """ Remember previous coordinates for scrolling with the mouse """
        self.canvas.scan_mark(event.x, event.y)

    def __move_to(self, event):
        """ Drag (move) canvas to the new position """
        self.canvas.scan_dragto(event.x, event.y, gain=1)
        self.__show_image()  # zoom tile and show it on the canvas

    def outside(self, x, y):
        """ Checks if the point (x,y) is outside the image area """
        bbox = self.canvas.coords(self.container)  # get image area
        if bbox[0] < x < bbox[2] and bbox[1] < y < bbox[3]:
            return False  # point (x,y) is inside the image area
        else:
            return True  # point (x,y) is outside the image area

    def __wheel(self, event):
        """ Zoom with mouse wheel """
        x = self.canvas.canvasx(event.x)  # get coordinates of the event on the canvas
        y = self.canvas.canvasy(event.y)
        if self.outside(x, y): return  # zoom only inside image area
        scale = 1.0
        # Respond to Linux (event.num) or Windows (event.delta) wheel event
        if event.num == 5 or event.delta == -120:  # scroll down, smaller
            if round(self.__min_side * self.imscale) < 30: return  # image is less than 30 pixels
            self.imscale /= self.__delta
            scale        /= self.__delta
            if self.imscale < self.get_scale(self.imcopy):
                pass
        if event.num == 4 or event.delta == 120:  # scroll up, bigger
            i = min(self.canvas.winfo_width(), self.canvas.winfo_height()) >> 1
            if i < self.imscale: return  # 1 pixel is bigger than the visible area
            self.imscale *= self.__delta
            scale        *= self.__delta
            #print(self.imscale == scale)
            
        # Take appropriate image from the pyramid
        k = self.imscale * self.__ratio  # temporary coefficient
        self.__curr_img = min((-1) * int(math.log(k, self.__reduction)), len(self.__pyramid) - 1)
        self.__scale = k * math.pow(self.__reduction, max(0, self.__curr_img))
        #
        self.canvas.scale('all', x, y, scale, scale)  # rescale all objects
        # Redraw some figures before showing image on the screen
        self.redraw_figures()  # method for child classes
        self.__show_image()

    def __keystroke(self, event):
        """ Scrolling with the keyboard.
            Independent from the language of the keyboard, CapsLock, <Ctrl>+<key>, etc. """
        if event.state - self.__previous_state == 4:  # means that the Control key is pressed
            pass  # do nothing if Control key is pressed
        else:
            self.__previous_state = event.state  # remember the last keystroke state
            # Up, Down, Left, Right keystrokes
            if event.keycode in [68, 39, 102]:  # scroll right: keys 'D', 'Right' or 'Numpad-6'
                self.__scroll_x('scroll',  1, 'unit', event=event)
            elif event.keycode in [65, 37, 100]:  # scroll left: keys 'A', 'Left' or 'Numpad-4'
                self.__scroll_x('scroll', -1, 'unit', event=event)
            elif event.keycode in [87, 38, 104]:  # scroll up: keys 'W', 'Up' or 'Numpad-8'
                self.__scroll_y('scroll', -1, 'unit', event=event)
            elif event.keycode in [83, 40, 98]:  # scroll down: keys 'S', 'Down' or 'Numpad-2'
                self.__scroll_y('scroll',  1, 'unit', event=event)

    def crop(self, bbox):
        """ Crop rectangle from the image and return it """
        if self.__huge:  # image is huge and not totally in RAM
            band = bbox[3] - bbox[1]  # width of the tile band
            self.__tile[1][3] = band  # set the tile height
            self.__tile[2] = self.__offset + self.imwidth * bbox[1] * 3  # set offset of the band
            self.__image.close()
            self.__image = self.baseimage  # reopen / reset image
            self.__image.size = (self.imwidth, band)  # set size of the tile band
            self.__image.tile = [self.__tile]
            return self.__image.crop((bbox[0], 0, bbox[2], band))
        else:  # image is totally in RAM
            return self.__pyramid[0].crop(bbox)

    def destroy(self):
        """ ImageFrame destructor """
        self.__image.close()
        map(lambda i: i.close, self.__pyramid)  # close all pyramid images
        del self.__pyramid[:]  # delete pyramid list
        del self.__pyramid  # delete pyramid variable
        self.canvas.destroy()
        self.__imframe.destroy()