import functions
import sys
import tkinter
import datetime
import os
import tkinter.scrolledtext as scrolledtext 
from tkinter import filedialog
import time
import datetime

# TODO: add title changing, entry deleting

def chunk(l, n):
    x = [l[i:i + n] for i in range(0, len(l), n)]
    return x


class TitleAsker:
    def __init__(self, master):
        self.master = master
        

        self.master.title("Save Entry")

        tkinter.Label(self.master, text="Entry title: ").grid(row=0)
        self.e1 = tkinter.Entry(self.master)
        self.e1.grid(row=0, column=1)

        tkinter.Button(self.master, text="Save Entry", command=self.save).grid(row=1)
    

    def save(self):
        title = self.e1.get()
        self.master.destroy()

    def run(self):
        self.master.mainloop()


class EntryChooser:
    def __init__(self, master, journal):
        self.master = master
        
        self.pages = chunk(list(journal.keys()), 5)

        self.master.title("Choose Entry")

        tkinter.Label(self.master, text="Page number: ").grid(row=0)
        
        self.page = tkinter.StringVar()
        self.previous = self.page.get()
        self.page.set("0")
        self.e1 = tkinter.Entry(self.master, textvariable=self.page)
        self.e1.grid(row=0, column=1)
        
        tkinter.Label(self.master, text="Entry title: ").grid(row=1)
        self.entry = tkinter.StringVar()
        self.entry.set(self.pages[0][0])
        self.menu = tkinter.OptionMenu(self.master, self.entry, *self.pages[int(self.e1.get())])
        self.menu.grid(row=1, column=1)


        tkinter.Button(self.master, text="Choose Entry", command=self.choose).grid(row=2)
        self.title = ""
    
    def onpagewrite(self, *args):
        text = self.page.get()
        try:
            text = int(text)
        except:
            if text == "":
                pass
            else:
                self.page.set(self.previous)
        else:
            if text >= len(self.pages):
                self.page.set(len(self.pages)-1)
            elif text < 0:
                self.page.set("0")
            self.previous = text
            self.entry.set(self.pages[int(self.page.get())][0])
            self.menu = tkinter.OptionMenu(self.master, self.entry, *self.pages[int(self.page.get())])
            self.menu.grid(row=1, column=1)

    def choose(self):
        if self.page.get() == "":
            self.title = self.pages[0][0]
        else:
            self.title = self.pages[int(self.page.get())][self.menu.get()]
        self.master.destroy()

    def run(self):
        self.page.trace("w", self.onpagewrite)
        self.master.mainloop()

class SaveAsker:
    def __init__(self, master):
        self.master = master
        

        self.master.title("Save?")

        tkinter.Label(self.master, text="Do you want to save your entry?").grid(row=0)
       
        tkinter.Button(self.master, text="Save", command=self.yes).grid(row=1)
        tkinter.Button(self.master, text="Don't Save", command=self.no).grid(row=1)
        tkinter.Button(self.master, text="Cancel", command=self.neither).grid(row=1)
        self.confirm = False
    

    def yes(self):
        self.confirm = True
        self.master.destroy()

    def no(self):
        self.confirm = False
        self.master.destroy()

    def neither(self):
        self.confirm = None
        self.master.destroy()

    def run(self):
        self.master.mainloop()


class JournalOpener:
    def __init__(self, master):
        self.master = master

        self.master.title("Journal Opener")

        tkinter.Button(self.master, text="Make New Journal", command=self.makenew).grid(row=0)
        tkinter.Button(self.master, text="Open Journal", command=self.openjournal).grid(row=1)

        self.journal = {}
        self.path = ""
        


    def makenew(self):
        filetypes = [("Encrypted File", ".enc")]
        path = os.path.dirname(os.path.realpath(__file__))
        savepath = filedialog.asksaveasfilename(parent=self.master,
                                      initialdir=path,
                                      filetypes=filetypes)
        if savepath == "":
            return

        encodedbytes = bytes(str(self.journal), encoding="utf-8")
        encrypted = functions.fernet.encrypt(encodedbytes)

        with open(savepath, "wb") as f:
            f.write(encrypted)


        self.path = savepath
        self.master.destroy()

    def openjournal(self):
        file = filedialog.askopenfilename()
        if file is None:
            return


        if not file.endswith(".enc"):
            return
        with open(file, "rb") as f:
            encrypted = f.read()
        data = functions.fernet.decrypt(encrypted, delete=False, silent=True)
        self.journal = data.decode("utf-8")
        self.path = file
        self.master.destroy()

    def run(self):
       
        self.master.mainloop()



class Journal:
    def __init__(self, master, path, journal):
        self.path = path
        self.master = master
        self.journal = journal

        self.menubar = tkinter.Menu(self.master)

        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Open Journal", command=self.openjournal)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)

        self.controls = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Journal Controls", menu=self.controls)
        self.controls.add_command(label="Open Entry", command=self.openentry)
        self.controls.add_command(label="Save Entry", command=self.saveentry)
        
        self.controls.add_command(label="Change Entry Title", command=self.quit)

        if len(self.journal.keys()) == 0:
            self.controls.entryconfig("Open Entry", state="disabled")

        self.entrytitle = ""
        self.savedtext = ""

        self.master.config(menu=self.menubar)

    def openjournal(self):
        opener = JournalOpener(tkinter.Tk())
        opener.run()
        self.journal = opener.journal
        self.display(list(self.journal.keys())[-1])

    def changetitle(self):
        pass


    def saveentry(self):
        text = self.textarea.get('1.0', tkinter.END)
        if self.entrytitle == "":
            asker = TitleAsker(tkinter.Tk())
            asker.run()
            title = asker.title
            dt = datetime.datetime.now()
            title = dt.strftime("%m/%d/%Y at %I:%M:%S %p") + ": " + title
            self.entrytitle = title
        self.journal[self.entrytitle] = text
        self.savedtext = text
        self.save()
        if len(self.journal.keys()) == 0:
            self.controls.entryconfig("Open Entry", state="normal")

    def save(self):
        encodedbytes = bytes(str(self.journal), encoding="utf-8")
        encrypted = functions.fernet.encrypt(encodedbytes)
        with open(self.path, "wb") as f:
            f.write(encrypted)

    def openentry(self):
        text = self.textarea.get('1.0', tkinter.END)
        if self.savedtext != text:
            asker = SaveAsker(tkinter.Tk())
            asker.run()
            confirm = asker.confirm
            if confirm is None:
                return
            elif not confirm:
                pass
            else:
                self.saveentry()
        chooser = EntryChooser(tkinter.Tk(), self.journal)
        chooser.run()
        title = chooser.title
        self.display(title)


    def quit(self):
        text = self.textarea.get('1.0', tkinter.END)
        if self.savedtext != text:
            asker = SaveAsker(tkinter.Tk())
            asker.run()
            confirm = asker.confirm
            if confirm is None:
                return
            elif not confirm:
                pass
            else:
                self.saveentry()
        self.master.destroy()

    def display(self, title):
        self.savedtext = self.journal[title]
        self.entrytitle = title
        self.textarea.insert("1.0", self.journal[title])

    def run(self):
        self.textarea = scrolledtext.ScrolledText(self.master, width=60, height=20)
        self.textarea.pack()
        
        self.master.mainloop()
        
if __name__ == "__main__":

    #EntryChooser(tkinter.Tk(), {x: x+1 for x in range(15)}).run()

    if not functions.login():
        sys.exit(1)
    path = ""
    while path == "":
        opener = JournalOpener(tkinter.Tk())
        opener.run()
        journal = opener.journal
        path = opener.path
    Journal(tkinter.Tk(), path, journal).run()