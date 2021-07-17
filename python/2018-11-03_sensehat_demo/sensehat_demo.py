import webbrowser
from threading import Thread
from time import sleep
from sense_hat import *

sense = SenseHat()
sense.clear()
def play():
	webbrowser.open('573817_DuoCore---The-Furious.mp3', True)

play_song = Thread(target = play)
play_song.start()
sleep(1.5)
R = [255, 0, 0]
x = [0, 0, 0]
sense.set_pixel(0, 7, R)
sleep(0.5)
sense.set_pixel(1, 7, R)
sleep(0.3)
sense.set_pixel(2, 7, R)
sleep(0.4)
sense.set_pixel(3, 7, R)
sleep(0.7)
sense.set_pixel(4, 7, R)
sleep(0.5)
sense.set_pixel(5, 7, R)
sleep(0.3)
sense.set_pixel(6, 7, R)
sleep(0.4)
sense.set_pixel(7, 7, R)
sleep(2.55)
first_map = [
x, x, x, x, x, x, x, x, 
x, x, x, x, x, x, x, x, 
x, x, x, x, x, x, x, R, 
x, x, x, x, R, x, R, R, 
x, x, x, R, R, x, R, R, 
x, R, x, R, R, x, R, R, 
x, R, R, R, R, R, R, R, 
R, R, R, R, R, R, R, R]
sense.set_pixels(first_map)
sleep(0.75)
sense.clear()
sleep(1.1)
sense.set_pixel(0, 0, R)
sleep(0.5)
sense.set_pixel(1, 0, R)
sleep(0.3)
sense.set_pixel(2, 0, R)
sleep(0.4)
sense.set_pixel(3, 0, R)
sleep(0.7)
sense.set_pixel(4, 0, R)
sleep(0.5)
sense.set_pixel(5, 0, R)
sleep(0.3)
sense.set_pixel(6, 0, R)
sleep(0.4)
sense.set_pixel(7, 0, R)
sleep(2.5)
current_map = [
R, R, R, R, R, R, R, R, 
R, R, R, R, R, R, R, x, 
R, R, x, R, R, R, R, x, 
R, x, x, R, R, R, x, x, 
R, x, x, x, R, x, x, x, 
x, x, x, x, R, x, x, x, 
x, x, x, x, x, x, x, x, 
x, x, x, x, x, x, x, x]
sense.set_pixels(current_map)
sleep(0.75)
sense.clear()
sleep(1.2)
sense.set_pixel(0, 3, R)
sense.set_pixel(1, 3, R)
sense.set_pixel(2, 3, R)
sense.set_pixel(3, 3, R)
sense.set_pixel(4, 3, R)
sense.set_pixel(5, 3, R)
sense.set_pixel(6, 3, R)
sense.set_pixel(7, 3, R)
sleep(0.5)
sense.set_pixel(0, 4, R)
sense.set_pixel(1, 4, R)
sense.set_pixel(2, 4, R)
sense.set_pixel(3, 4, R)
sense.set_pixel(4, 4, R)
sense.set_pixel(5, 4, R)
sense.set_pixel(6, 4, R)
sense.set_pixel(7, 4, R)
sleep(0.225)
sense.set_pixel(0, 2, R)
sense.set_pixel(1, 2, R)
sense.set_pixel(2, 2, R)
sense.set_pixel(3, 2, R)
sense.set_pixel(4, 2, R)
sense.set_pixel(5, 2, R)
sense.set_pixel(6, 2, R)
sense.set_pixel(7, 2, R)
sleep(0.5)
sense.set_pixel(0, 5, R)
sense.set_pixel(1, 5, R)
sense.set_pixel(2, 5, R)
sense.set_pixel(3, 5, R)
sense.set_pixel(4, 5, R)
sense.set_pixel(5, 5, R)
sense.set_pixel(6, 5, R)
sense.set_pixel(7, 5, R)
sleep(0.7)
