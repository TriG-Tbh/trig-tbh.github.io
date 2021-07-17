import cv2
import numpy as np
import os
from os.path import isfile, join
def convert_frames_to_video(pathIn,pathOut,fps):
    frame_array = []
    files = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f)) and not f.endswith(".mp4")]
    #for sorting the file names properly
    files.sort(key = lambda x: int(x[5:-4]))
    for i in range(len(files)):
        filename = os.path.join(pathIn, files[i])
        if i == 0 or i % 100 == 0:
            print("Frames complete: " + str(i))
        #reading each files
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        #inserting the frames into an image array
        frame_array.append(img)
    if i % 100 != 0:
        print("Frames complete: " + str(i + 1))
    out = cv2.VideoWriter(pathOut,cv2.VideoWriter_fourcc(*'MP4V'), fps, size)
    for i in range(len(frame_array)):
        # writing to a image array
        out.write(frame_array[i])
    out.release()
def main():
    os.system("cls")
    pathIn = input("Path to frames: ")
    pathOut = input("Path to video: ")
    fps = int(input("Framerate: "))
    convert_frames_to_video(pathIn, pathOut, fps)
if __name__=="__main__":
    main()