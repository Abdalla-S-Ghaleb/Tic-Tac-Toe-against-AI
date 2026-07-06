from math import inf


EMPTY = " "
X = "X"
O = "O"
HUMAN_MARK = X
BOT_MARK = O


def new_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]


def print_board(board):
    print()
    for i, row in enumerate(board):
        print(" " + " | ".join(row))
        if i < len(board) - 1:
            print("---+---+---")
    print()


def check_rows(board):
    for row in board:
        if row[0] != EMPTY and all(cell == row[0] for cell in row):
            return True
    return False


def check_columns(board):
    size = len(board)
    for col in range(size):
        first = board[0][col]
        if first != EMPTY and all(board[row][col] == first for row in range(size)):
            return True
    return False


def check_diagonals(board):
    size = len(board)
    first = board[0][0]
    if first != EMPTY and all(board[i][i] == first for i in range(size)):
        return True

    first = board[0][size - 1]
    if first != EMPTY and all(board[i][size - 1 - i] == first for i in range(size)):
        return True

    return False


def winner(board):
    size = len(board)

    for row in board:
        if row[0] != EMPTY and all(cell == row[0] for cell in row):
            return row[0]

    for col in range(size):
        first = board[0][col]
        if first != EMPTY and all(board[row][col] == first for row in range(size)):
            return first

    first = board[0][0]
    if first != EMPTY and all(board[i][i] == first for i in range(size)):
        return first

    first = board[0][size - 1]
    if first != EMPTY and all(board[i][size - 1 - i] == first for i in range(size)):
        return first

    return None


def Utility(board):
    game_winner = winner(board)
    if game_winner == X:
        return 1
    if game_winner == O:
        return -1
    return 0


def Terminal(board):
    return winner(board) is not None or not Actions(board)


def Actions(board):
    moves = []
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                moves.append((row, col))
    return moves


def Player(board):
    x_count = sum(row.count(X) for row in board)
    o_count = sum(row.count(O) for row in board)
    return X if x_count == o_count else O


def Result(board, action):
    row, col = action
    if board[row][col] != EMPTY:
        raise ValueError("That cell is already taken.")

    next_board = [current_row[:] for current_row in board]
    next_board[row][col] = Player(board)
    return next_board


def Min_Value(board):
    if Terminal(board):
        return Utility(board)

    value = inf
    for action in Actions(board):
        value = min(value, Max_Value(Result(board, action)))
    return value


def Max_Value(board):
    if Terminal(board):
        return Utility(board)

    value = -inf
    for action in Actions(board):
        value = max(value, Min_Value(Result(board, action)))
    return value


def Bot_Action(board):
    best_action = None

    if BOT_MARK == O:
        best_value = inf
        for action in Actions(board):
            value = Max_Value(Result(board, action))
            if value < best_value:
                best_value = value
                best_action = action
    else:
        best_value = -inf
        for action in Actions(board):
            value = Min_Value(Result(board, action))
            if value > best_value:
                best_value = value
                best_action = action

    row, col = best_action
    board[row][col] = BOT_MARK
    print(f"Bot chose row {row + 1}, column {col + 1}.")


def Player_Action(board):
    while True:
        move = input("Enter your move as row,column (example: 1,3): ").strip()
        parts = move.split(",")

        if len(parts) != 2:
            print("Please enter two numbers separated by a comma.")
            continue

        try:
            row = int(parts[0]) - 1
            col = int(parts[1]) - 1
        except ValueError:
            print("Please enter valid numbers.")
            continue

        if row not in range(3) or col not in range(3):
            print("Rows and columns must be between 1 and 3.")
            continue

        if board[row][col] != EMPTY:
            print("That cell is already taken.")
            continue

        board[row][col] = HUMAN_MARK
        break


def Play(first_to_play):
    global HUMAN_MARK, BOT_MARK

    if first_to_play == "Player":
        HUMAN_MARK = X
        BOT_MARK = O
    else:
        HUMAN_MARK = O
        BOT_MARK = X

    board = new_board()

    print(f"You are {HUMAN_MARK}. The bot is {BOT_MARK}.")
    print_board(board)

    while not Terminal(board):
        if Player(board) == HUMAN_MARK:
            Player_Action(board)
        else:
            Bot_Action(board)

        print_board(board)

    game_winner = winner(board)
    if game_winner == HUMAN_MARK:
        print("YOU WON!!")
    elif game_winner == BOT_MARK:
        print("YOU LOST :(")
    else:
        print("DRAW :|")


def end_game():
    while True:
        cont = input("Do you want to continue? (Y,N) ").strip().upper()
        if cont == "N":
            print("Good bye")
            return True
        if cont == "Y":
            print("Let's keep going!!!")
            return False
        print("Please enter a valid input.")


if __name__ == "__main__":
    games = 0
    while True:
        if games % 2 == 0:
            Play("Player")
        else:
            Play("Bot")

        games += 1
        if end_game():
            break
