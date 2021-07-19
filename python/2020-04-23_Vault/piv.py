from PIL import Image, ImageTk, ImageOps
import tkinter
from tkinter import filedialog
import functions
import getpass
import os

global imagepos
imagepos = 0

if __name__ == "__main__":
    functions.clear()
    password = getpass.getpass("Password: ")
    if not functions.login(password):
        import sys
        print("Invalid password")
        sys.exit(1)

functions.clear()

global images
images = []

global imagelabel


def handle_keypress(event):
    if str(event.keysym) == "Left":
        if imagepos > 0:
            back()
    if str(event.keysym) == "Right":
        try:
            _ = images[imagepos + 1]
        except:
            pass
        else:
            forward()
    if str(event.keysym) == "Escape":
        root.quit()


def forward():
    global imagepos, imagelabel
    imagelabel.grid_forget()
    #imagepos = (imagepos + 1) % len(images)
    imagepos += 1
    backbutton["state"] = "normal"
    try:
        _ = images[imagepos + 1]
    except:
        forwardbutton["state"] = "disabled"
    display_image(images)


def back():
    global imagepos, imagelabel
    imagelabel.grid_forget()
    imagepos -= 1
    forwardbutton["state"] = "normal"
    if imagepos == 0:
        backbutton["state"] = "disabled"
    display_image(images)


def get_image():
    path = filedialog.askopenfilename()
    load_image(path)


def get_folder():
    path = filedialog.askdirectory()
    load_directory(path)


def load_image(path):
    if path == ():
        return
    global images
    images = []
    if functions.validate(path):
        image = Image.open(path)
        width, height = image.size
        longer = (width if width > height else height)
        if longer > 750:
            ratio = 750 / longer
            if longer == width:
                width = 750
                height = int(round(height * ratio, 0))
            else:
                height = 750
                width = int(round(width * ratio, 0))
        image = image.resize((width, height), Image.ANTIALIAS)
        imgobj = ImageTk.PhotoImage(image)

        images.append(imgobj)
    if path.endswith(".enc"):
        temp = functions.decodepath(path, delete=False)
        if functions.validate(temp):
            image = Image.open(temp)
            width, height = image.size
            longer = (width if width > height else height)
            if longer > 750:
                ratio = 750 / longer
                if longer == width:
                    width = 750
                    height = int(round(height * ratio, 0))
                else:
                    height = 750
                    width = int(round(width * ratio, 0))
            image = image.resize((width, height), Image.ANTIALIAS)
            imgobj = ImageTk.PhotoImage(image)
            images.append(imgobj)
        os.remove(temp)
    display_image(images)


def load_directory(directory):
    global images, imagepos
    imagepos = 0
    if directory == ():
        return
    images = []
    if not os.path.isdir(directory):
        return
    files = [
        os.path.join(directory, f) for f in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, f))
    ]
    files = sorted(files)
    for file in files:
        if functions.validate(file):
            image = Image.open(file)
            width, height = image.size
            longer = (width if width > height else height)
            if longer > 750:
                ratio = 750 / longer
                if longer == width:
                    width = 750
                    height = int(round(height * ratio, 0))
                else:
                    height = 750
                    width = int(round(width * ratio, 0))
            image = image.resize((width, height), Image.ANTIALIAS)
            imgobj = ImageTk.PhotoImage(image)
            images.append(imgobj)
        if file.endswith(".enc"):
            temp = functions.decodepath(file, delete=False)
            if functions.validate(temp):
                image = Image.open(temp)
                width, height = image.size
                longer = (width if width > height else height)
                if longer > 750:
                    ratio = 750 / longer
                    if longer == width:
                        width = 750
                        height = int(round(height * ratio, 0))
                    else:
                        height = 750
                        width = int(round(width * ratio, 0))
                image = image.resize((width, height), Image.ANTIALIAS)
                imgobj = ImageTk.PhotoImage(image)
                images.append(imgobj)
            os.remove(temp)

    global forwardbutton
    if len(images) > 1:
        forwardbutton["state"] = "normal"
    display_image(images)


def display_image(images):
    global imagelabel, imagepos
    if len(images) < 1:
        imagelabel = tkinter.Label()
    else:
        imagelabel = tkinter.Label(image=images[imagepos])
    global backbutton
    backbutton = tkinter.Button(root,
                                text="<<",
                                command=back,
                                state=tkinter.DISABLED)

    global forwardbutton
    forwardbutton = tkinter.Button(root,
                                   text=">>",
                                   command=forward,
                                   state=tkinter.DISABLED)
    if imagepos > 0:
        backbutton["state"] = "normal"
    if len(images) > 1 and (imagepos + 1) < len(images):
        forwardbutton["state"] = "normal"

    imagelabel.grid(row=1, column=0, columnspan=5)
    backbutton.grid(row=0, column=0)
    forwardbutton.grid(row=0, column=4)
    if len(images) > 0:
        height = images[imagepos].height() + 33
        width = images[imagepos].width()
        root.geometry("{}x{}".format(width + 1, height))
        root.update()


root = tkinter.Tk()
root.lift()
root.attributes('-topmost', True)
root.after_idle(root.attributes, '-topmost', False)
root.title("Private Image Viewer")

global directory

global imagelabel
#imagelabel = tkinter.Label(image=images[0])
imagelabel = tkinter.Label()

imagebutton = tkinter.Button(root, text="Select Image", command=get_image)
exitbutton = tkinter.Button(root, text="Exit PIV", command=root.quit)
folderbutton = tkinter.Button(root, text="Select Folder", command=get_folder)

imagebutton.grid(row=0, column=1)
exitbutton.grid(row=0, column=2)
folderbutton.grid(row=0, column=3)

global backbutton
backbutton = tkinter.Button(root,
                            text="<<",
                            command=back,
                            state=tkinter.DISABLED)

global forwardbutton
forwardbutton = tkinter.Button(root,
                               text=">>",
                               command=forward,
                               state=tkinter.DISABLED)

# load_directory(directory)
# display_image(images)
"""
imagelabel.grid(row=0, column=0, columnspan=5)
backbutton.grid(row=1, column=0)
forwardbutton.grid(row=1, column=4)
"""
root.bind("<Key>", handle_keypress)


def main():
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.quit()


if __name__ == "__main__":
    main()
