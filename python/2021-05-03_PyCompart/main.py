import tkinter as tk
import tkinter.filedialog as fd
import os
import tkinter.messagebox as mb

variables = ["Read Only", "Use Virtual GPU", "Enable Internet Access", "Audio Input", "Video Input", "Bidirectional Copying"]
intvars = []

root = tk.Tk()
root.title("PyCompart")

root.geometry("250x255")
root.pack_propagate(0)



global file
file = None

def openfile():
    global file
    f = fd.askopenfilename()
    if f:
        file = f

        filedesc.config(text="File: " + str(os.path.basename(file)))
        
        

def onclick():
    global file
    if not file: return
    settings = {}
    for i in range(len(intvars)):
        settings[variables[i]] = intvars[i].get()
    files = [("Sandbox Configuration File", "*.wsb")]
    savefile = fd.asksaveasfilename(filetypes = files, defaultextension = files)
    if not savefile: return

    text = "<Configuration>\n"
    basedir = os.path.basename(os.path.dirname(file))
    text = text + "<MappedFolders><MappedFolder><HostFolder>" + os.path.dirname(file) + "</HostFolder>" + ("<ReadOnly>true</ReadOnly>" if settings["Read Only"] else "") + "<SandboxFolder>C:\\Users\\WDAGUtilityAccount\\Desktop\\" + basedir + "</SandboxFolder></MappedFolder></MappedFolders>"
    filename = os.path.basename(file)
    text = text + "<LogonCommand><Command>" + "\"C:\\Users\\WDAGUtilityAccount\\Desktop\\" + basedir + "\\" + filename + "\"</Command></LogonCommand>"

    if settings["Use Virtual GPU"]: text = text + "<VGpu>Enable</VGpu>"
    if not settings["Enable Internet Access"]: text = text + "<Networking>Disable</Networking>"
    if not settings["Audio Input"]: text = text + "<AudioInput>Disable</AudioInput>"
    if settings["Video Input"]: text = text + "<VideoInput>Enable</VideoInput>"
    if not settings["Bidirectional Copying"]: text = text + "<ClipboardRedirection>Disable</ClipboardRedirection>"

    text = text + "</Configuration>"

    with open(savefile, "w") as f:
        f.write(text)

    mb.showinfo(title="PyCompart", message="Config file successfully saved.")
    


openbutton = tk.Button(root,text="Open...",command=openfile)
openbutton.pack(anchor="s")

filedesc = tk.Label(root, text="File: " + str(file))
filedesc.pack(fill=tk.BOTH, expand=1)


tk.Label(text="Options:").pack(anchor="w")


for v in variables:
    iv = tk.IntVar()
    intvars.append(iv)
    tk.Checkbutton(root, text = v, variable=iv).pack(anchor="w")
 



savebutton = tk.Button(root,text="Save...",command=onclick)
savebutton.pack(anchor="s", pady=5)




root.mainloop()