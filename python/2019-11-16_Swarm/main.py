import random

blank = "\u001b[30m" + "■" + "\u001b[0m"
p1 = "\u001b[31;1m" + "■" + "\u001b[0m"
p2 = "\u001b[34;1m" + "■" + "\u001b[0m"
powerup = "\u001b[32;1m" + "■" + "\u001b[0m"

ROWS = 7
COLUMNS = 10

class Space():
    def __init__(self, id, x=None, y=None):
        if x is not None:
            self.x = x
        if y is not None:
            self.y = y
        self.id = id
        self.image = ""
        if self.id == 0:
            self.image = blank
        if self.id == 1:
            self.image = p1
        if self.id == 2:
            self.image == p2
        if self.id == 3:
            self.image = powerup
    
    def move(self):
        direction = random.randint(1, 4)
        if direction == 1:
            self.x += 1
        if direction == 2:
            self.x -= 1
        if direction == 3:
            self.y += 1
        if direction == 4:
            self.y -= 1
        if self.y < 0:
            self.y = 0
        if self.y >= ROWS:
            self.y = ROWS - 1
        if self.x < 0:
            self.x = 0
        if self.y >= COLUMNS:
            self.y = COLUMNS - 1

    


board = []
for _ in range(ROWS):
    line = []
    for _ in range(COLUMNS):
        line.append(Space(0))
    board.append(line)

def print_board(board):
    message = ""
    for row in board:
        line = " ".join([item.image for item in row])
        message += line + "\n"
    message = message.strip()
    print(message)

pieces = []
def update_pieces(pieces):
    for piece in pieces:
        if piece.x is not None and piece.y is not None:
            board[piece.oldy][piece.oldx] = blank
            board[piece.y][piece.x] = piece


player1 = Space(1, x=2, y=3)
player1.move()
#player2 = Space(2, x=7, y=3)

pieces.append(player1)
#pieces.append(player2)
update_pieces(pieces)

print_board(board)

player1.move()
update_pieces(pieces)
print_board(board)