import os
import platform
import random
import time
import math

COLUMN_COUNT = 7
ROW_COUNT = 6
WINDOW_COUNT = 4

if platform.system() == "Darwin" and platform.machine().startswith("iP"):
    p1_piece = "R"
    p2_piece = "Y"
    blank_piece = "B"
    position_arrow = "↓"
else:
    p1_piece = "\u001b[31;1m" + "■" + "\u001b[0m"
    p2_piece = "\u001b[33;1m" + "■" + "\u001b[0m"
    blank_piece = "\u001b[30m" + "■" + "\u001b[0m"
    position_arrow = "\u001b[32;1m" + "↓" + "\u001b[0m"

def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        if platform.system() == "Darwin" and platform.machine().startswith("iP"):
            try:
                import console
                console.clear()
            except ImportError:
                pass


def create_board():
    board = []
    for _ in range(ROW_COUNT):
        line = []
        for _ in range(COLUMN_COUNT):
            line.append(0)
        board.append(line)
    return board


def print_board(board):
    strboard = str(board[::-1])
    strboard = strboard.replace("]]", "]")
    strboard = strboard.replace("]", "\n")
    strboard = strboard.replace("[", "")
    strboard = strboard.replace(".", "")
    strboard = strboard.replace(", ", " ")
    strboard = strboard.replace("0", blank_piece)
    strboard = strboard.replace("1", p1_piece)
    strboard = strboard.replace("2", p2_piece)
    strboard = strboard.replace("\n ", "\n")
    strboard = strboard.strip()
    print(strboard)


def drop_piece(board, row, col, piece):
    board[row][col] = piece
    return board


def is_valid_location(board, col):
    try:
        return board[ROW_COUNT - 1][col] == 0
    except:
        return False


def get_next_open_row(board, col):
    for row in range(ROW_COUNT):
        if board[row][col] == 0:
            return row


def winning_move(board, piece):
    for r in range(ROW_COUNT):
        row_array = [i for i in list(board[r][:])]
        for c in range(COLUMN_COUNT - (WINDOW_COUNT - 1)):
            window = row_array[c:c+WINDOW_COUNT]
            if window.count(piece) == 4:
                return True

    for c in range(COLUMN_COUNT):
        col_array = []
        for row in board:
            col_array.append(row[c])
        for r in range(ROW_COUNT - (WINDOW_COUNT - 1)):
            window = col_array[r:r+WINDOW_COUNT]
            if window.count(piece) == 4:
                return True

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_COUNT)]
            if window.count(piece) == 4:
                return True

    for r in range(len(board) - 3):
        for c in range(len(board[0]) - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_COUNT)]
            if window.count(piece) == 4:
                return True
    return False


def random_move():
    return random.randint(0, COLUMN_COUNT-1)


def score_window(window, piece):
    score = 0
    opp_piece = (1 if piece == 2 else 2)
    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(0) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(0) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(0) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0
    for r in range(ROW_COUNT):
        row_array = [i for i in list(board[r][:])]
        for c in range(COLUMN_COUNT - (WINDOW_COUNT - 1)):
            window = row_array[c:c+WINDOW_COUNT]
            score += score_window(window, piece)

    for c in range(COLUMN_COUNT):
        col_array = []
        for row in board:
            col_array.append(row[c])
        for r in range(ROW_COUNT - (WINDOW_COUNT - 1)):
            window = col_array[r:r+WINDOW_COUNT]
            score += score_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+i][c+i] for i in range(WINDOW_COUNT)]
            score += score_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r+3-i][c+i] for i in range(WINDOW_COUNT)]
            score += score_window(window, piece)

    return score


def copy(board):
    new = []
    for row in board:
        line = []
        for item in row:
            line.append(item)
        new.append(line)
    return new


def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_column = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = copy(board)
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_column = col
    return best_column

def is_terminal_node(board):
    return winning_move(board, 1) or winning_move(board, 2) or is_tie(board)


def minimax(board, depth, alpha, beta, maximizingplayer, piece):
    board = board.copy()
    opp_piece = (1 if piece == 2 else 2)
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, piece):
                return (None, 10000000000000)
            elif winning_move(board, opp_piece):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, piece))
    if maximizingplayer:
        column = random.choice(valid_locations)
        value = -math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            bcopy = copy(board)
            drop_piece(bcopy, row, col, piece)
            new_score = minimax(bcopy, depth - 1, alpha, beta, False, piece)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value

    else:
        column = random.choice(valid_locations)
        value = math.inf
        for col in valid_locations:
            row = get_next_open_row(board, col)
            bcopy = copy(board)
            drop_piece(bcopy, row, col, opp_piece)
            new_score = minimax(bcopy, depth - 1, alpha, beta, True, piece)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def ai_turn(board, turn, difficulty):
    #depth = (difficulty - 2) * 2
    depth = 7
    newboard = board.copy()
    print("Player {}, make your selection (1-7): ".format(turn + 1),
          end="", flush=True)
    start = time.time()
    if difficulty == 1:
        col = random_move()
    elif difficulty == 2:
        col = pick_best_move(newboard, turn + 1)
    elif difficulty >= 3:
        col, _ = minimax(newboard, depth, -math.inf, math.inf, True, turn + 1)
    rejected = not is_valid_location(board, col)
    while rejected:
        if difficulty == 1:
            col = random_move()
        elif difficulty == 2:
            col = pick_best_move(newboard, turn + 1)
        elif difficulty >= 3:
            col, _ = minimax(newboard, depth, -math.inf, math.inf, True, turn + 1)
        rejected = not is_valid_location(board, col)
    if (time.time() - start) < 1:
        time.sleep(1)
    print(col + 1)
    time.sleep(0.6)
    return col


def player_turn(turn):
    col = input("Player {}, make your selection (1-7): ".format(turn + 1))
    try:
        col = int(col) - 1
    except:
        return None
    else:
        return col


def is_tie(board):
    valid_locations = get_valid_locations(board)
    if len(valid_locations) == 0:
        return True
    return False


def print_line():
    line = []
    for _ in range(COLUMN_COUNT):
        line.append("-")
    print(" ".join(line))

def solve():
    board = create_board()
    clear()
    first = ""
    while first not in ["1", "2"]:
        first = input("Select who is going first:\n1: Opponent\n2: You + Bot\nSelect an option: ")
        first = first.strip().lower()
        clear()
    depth = ""
    gettingdepth = True
    while gettingdepth:
        depth = input("Enter the number of moves to look ahead (preferably 3-6): ")
        depth = depth.strip().lower()
        try:
            depth = int(depth)
        except:
            continue
        else:
            gettingdepth = False
    aimove = False
    if first == "1":
        aimove = False
    else:
        aimove = True
    turn = 0
    while True:
        clear()
        print_line()
        print_board(board)
        if aimove:
            print("Calculating...")
            newboard = board.copy()
            col, _ = minimax(newboard, depth, -math.inf, math.inf, True, turn + 1)
            rejected = not is_valid_location(board, col)
            while rejected:
                col, _ = minimax(newboard, depth, -math.inf, math.inf, True, turn + 1)
                rejected = not is_valid_location(board, col)
            clear()
            spacesbefore = col
            spacesafter = (COLUMN_COUNT - 1) - col
            printline = []
            for _ in range(spacesbefore):
                printline.append("-")
            printline.append(position_arrow)
            for _ in range(spacesafter):
                printline.append("-")
            print(" ".join(printline))
            print_board(board)
            print("Best possible column: {}".format(col + 1))
            input("Press enter to continue. ")
        else:
            col = input("Enter the column number of the opponent's move (1: leftmost column, 7: rightmost column, etc.): ")
            try:
                col = int(col) - 1
            except:
                continue

        if not is_valid_location(board, col):
            continue

        row = get_next_open_row(board, col)
        board = drop_piece(board, row, col, turn + 1)

        clear()
        print_line()
        print_board(board)
        if winning_move(board, turn + 1):
            if aimove:
                print("You win!")
                break
            else:
                print("Opponent wins.")

        if is_tie(board):
            print("Tie! No player wins.")
            break

        turn = (turn + 1) % 2
        aimove = not(aimove)


def play():
    board = create_board()
    clear()

    players = ""
    while players not in ["0", "1", "2"]:
        players = input("Enter number of players (0-2): ").strip()
        clear()
    players = int(players)

    aimove = None
    if players == 1:
        difficulty = ""
        while difficulty not in ["1", "2", "3", "4", "5"]:
            difficulty = input("Difficulty:\n1: Easy (Random column)\n2: Medium (Board scanning)\n3: Hard (Minimaxing, depth of 2 turns)\n4: Difficult (Minimaxing, depth of 4 turns)\n5: Extremely difficult (Minimaxing, depth of 6 turns)\nPick a difficulty: ")
            difficulty = difficulty.strip().lower()
            clear()
        difficulty = int(difficulty)
        aimove = random.choice([True, False])
        clear()
        if aimove:
            input("The AI will go first. Press enter to continue. ")
        else:
            input("You will go first. Press enter to continue. ")
    if players == 0:
        strategies = {
            1: "Random column",
            2: "Board scanning",
            3: "Minimaxing, depth of 2 turns", 
            4: "Minimaxing, depth of 4 turns",
            5: "Minimaxing, depth of 6 turns"
        }
        #p1_difficulty = random.randint(1, 5)
        #p2_difficulty = random.randint(1, 5)
        p1_difficulty = 5
        p2_difficulty = 5
        input("Player 1's strategy: {}\nPlayer 2's strategy: {}\nPress enter to continue. ".format(strategies[p1_difficulty], strategies[p2_difficulty]))

    turn = 0

    clear()
    print_board(board)

    while True:
        clear()
        print_board(board)
        if players == 2:
            col = player_turn(turn)
            if col is None:
                continue
        elif players == 1:
            if aimove:
                col = ai_turn(board, turn, difficulty)
            else:
                col = player_turn(turn)
                if col is None:
                    continue
        else:
            if turn == 0:
                col = ai_turn(board, turn, p1_difficulty)
            else:
                col = ai_turn(board, turn, p2_difficulty)

        if not is_valid_location(board, col):
            continue

        row = get_next_open_row(board, col)
        board = drop_piece(board, row, col, turn + 1)

        clear()
        print_board(board)

        if winning_move(board, turn + 1):
            print("Player {} wins!".format(turn + 1))
            break

        if is_tie(board):
            print("Tie! No player wins.")
            break

        turn = (turn + 1) % 2
        if aimove is not None:
            aimove = not(aimove)


def main():
    while True:
        try:
            clear()
            option = ""
            while option not in ["1", "2"]:
                option = input("Select an option:\n1: Play a game of Connect 4\n2: Use the AI to help you win a game of Connect 4\nSelect an option: ")
                option = option.strip().lower()
                clear()
            if option == "1":
                play()
            else:
                solve()
            input("Press enter to continue. ")
        except:
            input("\nUser requested an interrupt. Press enter to continue. ")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nUser exited script.")
