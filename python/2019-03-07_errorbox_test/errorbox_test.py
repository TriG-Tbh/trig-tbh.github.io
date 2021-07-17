import tkinter
from tkinter import messagebox
import pynput

# hide main window
root = tkinter.Tk()
root.withdraw()

# message box display

for i in range(1, 6):
    messagebox.showerror("Error", "Website has been blocked.")
