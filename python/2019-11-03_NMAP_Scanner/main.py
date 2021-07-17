import nmap
import sys
import os
import platform


def clear():
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass


scanner = nmap.PortScanner()
clear()
ip = input("IP address to be scanned: ")
clear()
scantype = input("""Type of scans: 
    1: SYN ACK Scan
    2: UDP Scan
    3: Comprehensive Scan
Enter one of the options: """)
scantype = scantype.strip()
scans = ["1", "2", "3"]
if scantype not in scans:
    sys.exit("Please select one of the options.")
clear()
if scantype == "1":
    print("Nmap Version: " + str(scanner.nmap_version()))
    scanner.scan(ip, '1-1024', '-v -sS')
    print(scanner.scaninfo())
    print("IP Status: " + str(scanner[ip].state()))
    