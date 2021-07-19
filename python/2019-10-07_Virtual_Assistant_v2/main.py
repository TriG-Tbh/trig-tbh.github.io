import speech_recognition as sr
import os
import sys
import re
import webbrowser
import smtplib
import requests
import subprocess
from pyowm import OWM
import youtube_dl
import vlc
import urllib3
import urllib
import json
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import wikipedia
import random
from time import strftime

def myCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Say something...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=1)
        audio = r.listen(source)
    try:
        command = r.recognize_google(audio).lower()
        print("Command: " + command + "\n")
    except sr.UnknownValueError:
        print("....")
        command = myCommand();
    return command

def response(audio):
    print(audio)
    for line in audio.splitlines():
        os.system("echo " + audio)

def assistant(command):
    if 'open reddit' in command:
        reg_ex = re.search("open reddit (.*)", command)
        url = "https://www.reddit.com/"

while True:
    assistant(myCommand())