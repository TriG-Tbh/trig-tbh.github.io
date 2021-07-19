import colorama
colorama.init()

dot = "■"
filled = "■"


def printboard(board):
    message = ""
    for line in board:
        message += "".join(line) + "\n"
    message = message.strip()
    print(message)


def createboard(x, y):
    line = dot*x
    line = [c for c in " ".join(line)]
    board = []
    for _ in range(y):
        board.append(line.copy())
        space = " " * len(line)
        board.append([c for c in space].copy())
    board = board[:-1]
    return board


def check(board, pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2
    board = board.copy()
    if not ((abs(x2 - x1) == 1 and y1 == y2) or (x1 == x2 and abs(y2 - y1) == 1)):
        return None
    if y2 > y1:
        posx, posy = (x2 * 2), (y2 * 2) - 1
    elif y1 > y2:
        posx, posy = (x2 * 2), (y2 * 2) + 1
    elif x2 > x1:
        posx, posy = (x2 * 2) - 1, (y2 * 2)
    elif x1 > x2:
        posx, posy = (x2 * 2) + 1, (y2 * 2)
    if x1 == x2:
        if posx != 0:
            try:
                if board[posy-1][posx-1].startswith(color) and board[posy][posx-2].startswith(color) and board[posy+1][posx-1].startswith(color):
                    board[posy][posx-1] = color + filled
            except IndexError:
                pass
        try:
            if board[posy-1][posx+1].startswith(color) and board[posy][posx+2].startswith(color) and board[posy+1][posx+1].startswith(color):
                board[posy][posx+1] = color + filled
        except IndexError:
            pass
    if y1 == y2:
        if posy != 0:
            try:
                if board[posy-1][posx-1].startswith(color) and board[posy-2][posx].startswith(color) and board[posy-1][posx+1].startswith(color):
                    board[posy-1][posx] = color + filled
            except IndexError:
                pass
        try:
            if board[posy+1][posx+1].startswith(color) and board[posy+2][posx].startswith(color) and board[posy+1][posx-1].startswith(color):
                board[posy+1][posx] = color + filled
        except IndexError:
            pass
    return board


def place(board, pos1, pos2, color):
    x1, y1 = pos1
    x2, y2 = pos2
    board = board.copy()
    if not ((abs(x2 - x1) == 1 and y1 == y2) or (x1 == x2 and abs(y2 - y1) == 1)):
        return None
    if x2 > x1:
        piece = "-"
        posx, posy = (x2 * 2) - 1, (y2 * 2)
    if x1 > x2:
        piece = "-"
        posx, posy = (x2 * 2) + 1, (y2 * 2)
    if y2 > y1:
        piece = "|"
        posx, posy = (x2 * 2), (y2 * 2) - 1
    if y1 > y2:
        piece = "|"
        posx, posy = (x2 * 2), (y2 * 2) + 1
    board[posy][posx] = color + piece + '\033[39m'

    board = check(board, pos1, pos2, color)
    return board
