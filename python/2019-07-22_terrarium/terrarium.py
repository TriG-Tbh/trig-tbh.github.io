from time import sleep
import os
from colorama import Fore

os.system("clear")

print(str(Fore.BLACK))

board = [

]

length = int(input("Length: "))
width = int(input("Width: "))

def new():
    board = []
    for l in range(length):
        newline = []
        for w in range(width):
            newline.append(Fore.BLACK + "■")
        board.append(newline)
    return board

board = new()

blank = board

def printboard(board):
    os.system("clear")
    for line in board:
        print(" ".join(line))

#printboard(board)
os.system("clear")

def update(board):
    os.system("clear")
    sboard = new()
    x = 0
    for line in board:
        y = 0
        for cell in line:
            n = 0
            ns = []
            
            xpl1 = x + 1
            xsub1 = x - 1
            ypl1 = y + 1
            ysub1 = y - 1

            if xsub1 < 0:
                xsub1 = 876587436587643587463587436578463587643259872652876
            if ysub1 < 0:
                ysub1 = 876587436587643587463587436578463587643259872652876
            try:
                n1 = board[xsub1][ysub1]
            except:
                pass
            else:
                ns.append(n1)
            try:
                n2 = board[xsub1][y]
            except:
                pass
            else:
                ns.append(n2)
            try:
                n3 = board[xsub1][ypl1]
            except:
                pass
            else:
                ns.append(n3)
            try:
                n4 = board[x][ysub1]
            except:
                pass
            else:
                ns.append(n4)
            try:
                n5 = board[x][ypl1]
            except:
                pass
            else:
                ns.append(n5)
            try:
                n6 = board[xpl1][ysub1]
            except:
                pass
            else:
                ns.append(n6)
            try:
                n7 = board[xpl1][y]
            except:
                pass
            else:
                ns.append(n7)
            try:
                n8 = board[xpl1][ypl1]
            except:
                pass
            else:
                ns.append(n8)
            
            for ne in ns:
                if Fore.WHITE in ne:
                    n += 1
            if n == 3 and Fore.BLACK in cell:
                sboard[x][y] = Fore.WHITE + "■"
            if n < 2 and Fore.WHITE in cell:
                sboard[x][y] = Fore.BLACK + "■"
            if n > 3 and Fore.WHITE in cell:
                sboard[x][y] = Fore.BLACK + "■"
            if (n <= 3 and n >= 2) and Fore.WHITE in cell:
                sboard[x][y] = Fore.WHITE + "■"
            y += 1
        x += 1
    board = sboard
    printboard(board)
    return board


printboard(board)
while True:
    print(Fore.WHITE)
    menu = input("> ")
    if menu == "run":
        os.system("clear")
        printboard(board)
        sleep(1)
        while True:
            board = update(board)
            sleep(1)
    elif ", " in menu:
        x, y = menu.split(", ")
        x, y = int(x), int(y)
        try:
            pos = board[x][y]
        except:
            os.system("clear")
            printboard(board)
            print(Fore.WHITE)
            print("Invalid position")
        else:
            if Fore.BLACK in pos:
                board[x][y] = Fore.WHITE + "■"
            else:
                board[x][y] = Fore.BLACK + "■"
            os.system("clear")
            printboard(board)
    elif menu.startswith("new "):
        try:
            temp = menu.replace("new ", "")
            length, width = temp.split(" ")
            board = new()
            os.system("clear")
            printboard(board)
        except:
            os.system("clear")
            printboard(board)
            print(Fore.WHITE)
            print("Invalid arguments")