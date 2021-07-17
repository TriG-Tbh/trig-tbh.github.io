from tkinter import *
def get(s):
        print(s.get())
def newwin():
    win=Tk()
    s=StringVar()
    button=Button(win,text='click',command=lambda:get(s)).grid(row=1)
    ent=Entry(win,textvariable=s).grid()
root=Tk()
but=Button(root,text='New',command=newwin).grid()
