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

class Journal:
    def __init__(self, master):
        self.master = master
        
        self.menubar = tkinter.Menu(self.master)

        self.filemenu = tkinter.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="New Entry", command=self.createentry)
        self.filemenu.add_command(label="Open Entry", command=self.openentry)
        self.filemenu.add_command(label="Save Entry", command=self.saveentry)
        self.filemenu.add_command(label="Change Entry Title", command=self.quit)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)
        self.master.resizable(0,0)

        #self.filemenu.entryconfig("Save Entry", state="disabled")

        self.master.config(menu=self.menubar)

        self.path = ""

        self.time = ""
        self.date = ""
        self.title = ""
        self.text = ""

        self.saved = ""

    def changetitle(self):
        pass

    def gettime(self, path):
        file = os.path.realpath(path)
        print(file)
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
        entry = json.dumps({"title": self.title, "text": self.text})
        encrypted = functions.fernet.encrypt(entry.encode()).decode("utf-8")
        encrypted = encrypted + "|journal"
        encrypted = functions.fernet.encrypt(encrypted.encode())
        with open(self.path, "wb") as f:
            f.write(encrypted)
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
            contents = f.read()
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

        self.display(self.date + " ({}): ".format(self.time) + self.title)

    def quit(self):
        self.master.destroy()

    def display(self, title):
        self.saved = self.text
        self.master.title(title)
        self.textarea.delete("1.0", "end-1c")
        self.textarea.insert("1.0", self.text)

    def run(self):
        self.textarea = scrolledtext.ScrolledText(self.master, width=60, height=20, wrap=tkinter.WORD)
        self.textarea.pack()
        
        self.master.mainloop()
        

if __name__ == "__main__":
    if not functions.login():
        print("bad")
        sys.exit(1)
    Journal(tkinter.Tk()).run()
