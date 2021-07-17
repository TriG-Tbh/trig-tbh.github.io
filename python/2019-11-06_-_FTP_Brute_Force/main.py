import socket
import re
import sys

IP = "192.168.1.28" # Localhost
PORT = 21 # FTP Port



def connection(ip, user, password):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((IP, PORT))
    data = s.recv(1024)
    s.send("Username: " + user + "\r\n")