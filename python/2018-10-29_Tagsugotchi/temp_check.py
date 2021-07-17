from sense_hat import *
from time import sleep
from random import *
from threading import Thread
import pymsgbox

sense = SenseHat()
sense.clear()

def get_temp():
	while True:
		temp = sense.get_temperature()
		temp_f = ((temp*1.8)+32)
		temp = str(temp)
		temp_f = str(temp_f)
		print("Current temperature: " + temp + " C, " + temp_f + " F")
		temp = float(temp)
		temp_f = float(temp_f)
		if temp > 34.25:
			temp = str(temp)
			temp_f = str(temp_f)
			pymsgbox.alert('If you are reading this, the Raspberry Pi is working in unsafe environmental conditions.' + '\n' + 'The Pi is overheating at ' + temp + ' degrees Celsius, or ' + temp_f + ' degrees Fahrenheit.' + '\n' + 'Please stop whatever you are doing and cool down the Pi!', 'Computer Overheating!')
		sleep(1)
temp_check = Thread(target = get_temp)
temp_check.start()
	
