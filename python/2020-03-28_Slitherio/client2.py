import pygame
import socket
import os
import sys
import platform

def clear():
    plt = platform.system()
    if plt == "Linux" or plt == "Darwin":
        os.system("clear")
    elif plt == "Windows":
        os.system("cls")
    else:
        pass

connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pygame.init()

def main():
    clear()
    server = input("Server address: ")
    port = input("Port: ")
    try:
        connection.connect((server, port))
    except ConnectionRefusedError:
        print("Invalid address: {}:{}".format(server, port))
        sys.exit(1)
    win = pygame.display.set_mode((width, width))

