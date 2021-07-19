import functions
import os
from colorama import Fore


class Player:
    def __init__(self, color):
        self.color = color


board = functions.createboard(5, 5)
while True:
    os.system("cls")
    functions.printboard(board)
    p1 = input("Position 1: ")
    p1 = tuple(map(int, p1.split(', ')))
    p2 = input("Position 2: ")
    p2 = tuple(map(int, p2.split(', ')))
    functions.place(board, p1, p2, Fore.RED)
