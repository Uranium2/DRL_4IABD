

def print_board(game_board):
    header = [ i for i in range(len(game_board[0]))]
    print("  | ", end="")
    for i in header:
        print(str(i) + " | ", end="")
    print()
    print("--", "-" * len(game_board[0]) * 4)
    for i, row in enumerate(game_board):
        print(str(i) + " | ", end="")
        for item in row:
            print(item + " | ", end="")
        print()

def create_board(size):
    game_board = []
    i = size
    while i > 0:
        game_board.append([" " for size in range(size)])
        i = i - 1
    return game_board

def make_move(x, y, player, game_board):
    if player == 0:
        char = "X"
    else:
        char = "O"
    if (game_board[x][y] == " "):
        game_board[x][y] = char
    else:
        return False
    return True

def check_input(x, y, game_board):
    try:
        x = int(x)
        y = int(y)
    except ValueError:
        return False
    if x > len(game_board[0]) - 1 or x < 0 or y > len(game_board[0]) - 1 or y < 0:
        return False
    return True

def check_row_move(game_board):
    for i in range(len(game_board[0])):
        my_set = set(game_board[i])
        if(len(my_set)==1 and " " not in my_set):
            return False
    return True

def check_diag_move(game_board):
    my_set = set(game_board)
    if(len(my_set)==1 and " " not in my_set):
        return False
    return True

def check_next_move(game_board):
    row = check_row_move(game_board)
    transposed_game_board = list(zip(*game_board))
    column = check_row_move(transposed_game_board)
    diag1 = [ game_board[i][i] for i in range(len(game_board))]
    diag1 = check_diag_move(diag1)
    diag2 = [ row[-i-1] for i,row in enumerate(game_board)]
    diag2 = check_diag_move(diag2)
    return row and column and diag1 and diag2


def check_row_winner(game_board):
    for i in range(len(game_board[0])):
        my_set = set(game_board[i])
        if(len(my_set)==1 and " " not in my_set):
            return game_board[i][0]
    return False

def check_diag_winner(game_board):
    my_set = set(game_board)
    if(len(my_set)==1 and " " not in my_set):
        return game_board[0]
    return False

def check_winner(game_board):
    row = check_row_winner(game_board)
    transposed_game_board = list(zip(*game_board))
    column = check_row_winner(transposed_game_board)
    diag1 = [ game_board[i][i] for i in range(len(game_board))]
    diag1 = check_diag_winner(diag1)
    diag2 = [ row[-i-1] for i,row in enumerate(game_board)]
    diag2 = check_diag_winner(diag2)
    return row or column or diag1 or diag2

def play_tic_tac_toe(size):
    game_board = create_board(size)
    print_board(game_board)
    player = 0
    while check_next_move(game_board):
        print("Player", player)
        x = input("X :")
        y = input("Y :")
        if not check_input(x, y, game_board):
            print("Wrong input, please try again")
            continue
        if not make_move(int(x), int(y), player, game_board):
            print("Cannot play here, please try again")
            continue
        player = (player + 1) % 2
        print_board(game_board)

    return check_winner(game_board)

winner = play_tic_tac_toe(3)
print("Winner is :", winner)