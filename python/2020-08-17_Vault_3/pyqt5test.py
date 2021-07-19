import imageio
from tkinter import Tk, Label
from PIL import ImageTk, Image
from pathlib import Path
import threading
import tkinter as tk

video_name = r"[REDACTED]"
video = imageio.get_reader(video_name)

global images
images = [ImageTk.PhotoImage(Image.fromarray(image).resize((500, 500))) for image in video.iter_data()]

def stream(label):
    global images
    delay = 1
    
    label.after(delay, lambda: stream(label))
    
    label.config(image=frame_image)
    label.image = frame_image
    

if __name__ == "__main__":

    root = tk.Tk()
    my_label = tk.Label(root)
    my_label.pack()
    thread = threading.Thread(target=stream, args=(my_label,))
    thread.daemon = 1
    thread.start()
    root.mainloop()