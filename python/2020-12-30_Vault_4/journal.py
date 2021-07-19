import functions
import sys
import tkinter
import datetime
import os
import tkinter.scrolledtext as scrolledtext 
from tkinter import filedialog
import time
import datetime
import json
import zlib
import base64
import threading
from portablepiv import ImageViewer
import multiprocessing

class TitleAsker:
    def __init__(self, master):
        self.master = master
        self.title = ""

        self.master.title("Save Entry")

        tkinter.Label(self.master, text="Entry title: ").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Button(self.master, text="Save Entry", command=self.save).grid(row=1)
    

    def save(self):
        self.title = self.e1.get()
        self.master.quit()
        return self.master.destroy()

    def run(self):
        self.master.mainloop()

class SaveAsker:
    def __init__(self, master):
        self.master = master
        

        self.master.title("Save?")

        tkinter.Label(self.master, text="Do you want to save your entry?").grid(row=0)
       
        tkinter.Button(self.master, text="Save", command=self.yes).grid(row=1)
        tkinter.Button(self.master, text="Don't Save", command=self.no).grid(row=2)
        tkinter.Button(self.master, text="Cancel", command=self.neither).grid(row=3)
        self.confirm = False
    

    def yes(self):
        self.confirm = True
        self.master.quit()
        return self.master.destroy()

    def no(self):
        self.confirm = False
        self.master.quit()
        return self.master.destroy()

    def neither(self):
        self.confirm = None
        self.master.quit()
        return self.master.destroy()

    def run(self):
        self.master.mainloop()

class AtcEditor:
    def placeall(self):
        self.atc_choice = tkinter.OptionMenu(self.master, self.atc, *self.atcs)
        self.atc_choice.place(relx=.5, rely=0, anchor=tkinter.N)
        tkinter.Button(self.master,
            text="Move Up",
            command=self.goup).place(relx=0, rely=1/3, anchor=tkinter.W)
        tkinter.Button(self.master,
            text="Move Down",
            command=self.godown).place(relx=1, rely=1/3, anchor=tkinter.E)
        tkinter.Button(self.master,
            text="Add",
            command=self.add).place(relx=0, rely=2/3, anchor=tkinter.W)

        tkinter.Button(self.master,
            text="Remove",
            command=self.remove).place(relx=1, rely=2/3, anchor=tkinter.E)

        tkinter.Button(self.master,
            text="Save",
            command=self.quit).place(relx=.5, rely=1, anchor=tkinter.S)

    def __init__(self, master, atcs):
        self.master = master
        self.atcs = atcs
        self.atc = tkinter.StringVar(self.master)
        self.master.title("Edit Attachments")
        if len(self.atcs) > 1:
            self.atc.set(self.atcs[0])
        else:
            self.atc.set("")
        if self.atcs == []:
            self.atcs = [""]
        
        self.placeall()


    def goup(self):
        text = self.atc.get() 
        index = self.atcs.index(text)
        if index > 0:
            self.atcs[index], self.atcs[index - 1] = self.atcs[index - 1], self.atcs[index]
            self.placeall()

    def godown(self):
        text = self.atc.get() 
        index = self.atcs.index(text)
        if index < len(self.atcs) - 1:
            self.atcs[index], self.atcs[index + 1] = self.atcs[index + 1], self.atcs[index]
            self.placeall()

    def add(self):
        file = filedialog.askopenfilename()
        
        if file is None or file == ():
            return
        file = file.split("/")[-1]
        self.atcs.append(file)
        if self.atcs[0] == "": self.atcs = self.atcs[1:]
        self.placeall()
        

    def remove(self):
        text = self.atc.get() 
        self.atcs.remove(text)
        if len(self.atcs) > 0:
            self.atc.set(self.atcs[0])
        else:
            self.atc.set("")
        if self.atcs == []: self.atcs = [""]
        self.placeall()

    def onatcwrite(self, *args):
        #self.atc = self.atc.get()
        pass

    def run(self):
        self.atc.trace("w", self.onatcwrite)
        self.master.mainloop()
    
    def quit(self):
        if self.atcs == [""]: self.atcs = []
        self.master.quit()
        return self.master.destroy()

class Journal:
    def __init__(self, master):
        self.master = master
        
        self.menubar = tkinter.Menu(self.master)

        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New", command=self.createentry)
        self.filemenu.add_command(label="Open", command=self.openentry)
        self.filemenu.add_command(label="Save", command=self.saveentry)
        self.filemenu.add_command(label="Change Title", command=self.changetitle)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.master.resizable(0,0)


        self.attachmenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Attachments", menu=self.attachmenu)
        self.attachmenu.add_command(label="Open", command=self.openattachments)
        self.attachmenu.add_command(label="Edit", command=self.editattachments)

        self.attachmenu.entryconfig("Open", state="disabled")
        #self.attachmenu.entryconfig("Edit", state="disabled")

        self.filemenu.entryconfig("Change Title", state="disabled")

        self.master.config(menu=self.menubar)

        self.path = ""

        self.time = ""
        self.date = ""
        self.title = ""
        self.text = ""

        self.attachments = []

        self.saved = ""

    def changetitle(self):
        asker = TitleAsker(tkinter.Tk())
        asker.run()
        self.title = asker.title

    def openattachments(self):
        viewer = ImageViewer(tkinter.Toplevel(), self.attachments)
        viewer.run()


    def editattachments(self):
        atc = AtcEditor(tkinter.Toplevel(), self.attachments)
        atc.run()
        self.attachments = atc.atcs
        if len(self.attachments) > 0:
            try:
                self.attachmenu.entryconfig("Open", state="normal")
            except:
                pass
        else:
            try:
                self.attachmenu.entryconfig("Open", state="disabled")
            except:
                pass

    def gettime(self, path):
        file = os.path.realpath(path)
        if file is None:
            return
        #if not file.endswith(".enc"):
        #    return
        name = file.split(os.path.sep)[-1]
        floor = 1609353331.7162652
        ceil = time.time()
        filename = name.split(".")[0]
        try:
            filename = int(filename)
        except:
            return 
        if not ((floor <= filename) and (filename <= ceil)):
            return 
        return filename

    def createentry(self):
        text = self.textarea.get('1.0', "end-1c")
        if self.saved != text:
            asker = SaveAsker(tkinter.Tk())
            asker.run()
            confirm = asker.confirm
            if confirm is None:
                return
            elif not confirm:
                pass
            else:
                self.saveentry()
        
        self.path = ""

        self.time = ""
        self.date = ""
        self.title = ""
        self.text = ""

        self.saved = ""
        self.attachments = []
        self.display("")

    def saveentry(self):
        text = self.textarea.get('1.0', "end-1c")
        if self.title == "":
            asker = TitleAsker(tkinter.Tk())
            asker.run()
            self.title = asker.title
        
        if self.path == "":

            folder = filedialog.askdirectory()
            if folder is None:
                return
            entrytime = time.time()
            self.path = os.path.join(folder, str(int(entrytime // 1)) + ".enc")
        
        
        self.time = self.gettime(self.path)
        self.date = datetime.datetime.fromtimestamp(self.time).strftime("%m/%d/%Y at %I:%M:%S %p")
        
        self.save()
        

    def save(self):
        self.text = self.textarea.get('1.0', "end-1c")
        entry = json.dumps({"title": self.title, "text": self.text, "attachments": self.attachments})
        encrypted = functions.fernet.encrypt(entry.encode()).decode("utf-8")
        encrypted = encrypted + "|journal"
        encrypted = functions.fernet.encrypt(encrypted.encode())
        with open(self.path, "wb") as f:
            compressed = base64.b64encode(zlib.compress(encrypted))
            f.write(compressed)
        self.display(self.date + " ({}): ".format(self.time) + self.title)
        self.saved = self.text

    def openentry(self):
        text = self.textarea.get('1.0', "end-1c")
        
        if self.saved != text:
            asker = SaveAsker(tkinter.Tk())
            asker.run()
            confirm = asker.confirm
            if confirm is None:
                return
            elif not confirm:
                pass
            else:
                self.saveentry()

        file = filedialog.askopenfilename()
        file = os.path.realpath(file)
        if file is None:
            return
        if not file.endswith(".enc"):
            return
        name = file.split(os.path.sep)[-1]
        floor = 1609353331.7162652
        ceil = time.time()
        filename = name.split(".")[0]
        try:
            filename = int(filename)
        except:
            return
        if not (floor <= filename <= ceil):
            return
        with open(file, "rb") as f:
            double_encrypted = f.read()
        
        contents = zlib.decompress(base64.b64decode(double_encrypted))
        decrypted = functions.fernet.decrypt(contents).decode("utf-8")
        contents, filetype = decrypted.split("|")
        if filetype != "journal":
            return
        decrypted = functions.fernet.decrypt(contents.encode()).decode("utf-8")
        entry = json.loads(decrypted)

        self.path = file

        self.time = filename
        self.date = datetime.datetime.fromtimestamp(filename).strftime("%m/%d/%Y at %I:%M:%S %p")
        self.title = entry["title"]
        self.text = entry["text"]
        self.attachments = entry["attachments"]
        if len(self.attachments) > 0:
            self.attachmenu.entryconfig("Open", state="normal")
        self.attachmenu.entryconfig("Edit", state="normal")

        self.display(self.date + " ({}): ".format(self.time) + self.title)

    def quit(self):
        self.master.destroy()

    def display(self, title):
        self.saved = self.text
        self.master.title(title)
        self.textarea.delete("1.0", "end-1c")
        self.textarea.insert("1.0", self.text)
        self.filemenu.entryconfig("Change Title", state="normal")

    def run(self):
        self.textarea = scrolledtext.ScrolledText(self.master, width=60, height=20, wrap=tkinter.WORD)
        self.textarea.pack()
        
        self.master.mainloop()
        

if __name__ == "__main__":
    #if not functions.login():
    #    print("bad")
    #    sys.exit(1)
    functions.key_login(key="[REDACTED]")
    Journal(tkinter.Tk()).run()
