# Script that copies streams from 7anime, downloads the series info, and packages it all into .strm and .nfo files for Kodi

import os
import platform

def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        pass



while True:
    action = "-1"
    while action not in ["1", "2"]:
        clear()
        action = input("""1: Download single stream
2: Download multiple streams (show, movie compilation, etc.)
Pick an option: """)
        action = action.strip().lstrip().lower()
    
    