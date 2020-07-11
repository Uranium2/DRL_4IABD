import numpy as np


def create_tic_tac(w, h):
    # [1 0 0] = empty , [0 1 0] = nos pions, [0 0 1] = pions ennemis
    map = [[1, 0, 0] for i in range(9)]
    num_states = w * h
    S = np.arange(num_states)
    A = np.arange(num_states)

def step_tic_tac(state, a, s_terminal, s_sp, player):

    if player == 0:
        pin_me = [0, 1, 0]
        pin_ennemy = [0, 0, 1]
    if player == 1:
        pin_me = [0, 0, 1]
        pin_ennemy = [0, 1, 0]
    # get the actual state from the ID

    state_board = s_sp[0][state]

    # Place the cursor

    l_board = []
    for s in state_board:
        for i in s:
            l_board.append(i)
    while(l_board[a] != [1, 0, 0]):
        a = np.random.choice(np.arange(9))
    l_board[a] = pin_me

    state_board = []
    state_board.append(l_board[:3])
    state_board.append(l_board[3:6])
    state_board.append(l_board[6:])
    state_sp = s_sp[1][str(state_board)]

    if s_terminal[state] == pin_me:
        is_terminal = True
        r = 1
    if s_terminal[state] == pin_ennemy:
        is_terminal = True
        r = -1
    if s_terminal[state] == [1, 0, 0]:
        is_terminal = False
        r = 0

    return state_sp, r, is_terminal  # position, reward, si terminal



def is_terminate_tic_tac(s, states):
    if states[s] == [1, 0, 0]:
        return False
    return True

def check_terminal_states(s):
    for i in range(3):
        if (s[i][0][1:] == s[i][1][1:] and s[i][0][1:] == s[i][2][1:] and s[i][0][0] != 1):
            return s[i][0]

    for i in range(3):
        if (s[0][0][1:] == s[1][0][1:] and s[0][0][1:] == s[2][0][1:] and s[0][0][0] != 1):
            return s[i][0]

    if (s[0][0][1:] == s[1][1][1:] and s[0][0][1:] == s[2][2][1:] and s[0][0][0] != 1):
        return s[i][0]

    if (s[0][2][1:] == s[1][1][1:] and s[0][0][1:] == s[2][0][1:] and s[0][2][0] != 1):
        return s[i][0]

    for l in range(3):
        for r in range(3):
            if s[l][r] == [1, 0, 0]:
                return [1, 0, 0]
    return [1, 1, 1]















    
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

# winner = play_tic_tac_toe(3)
# print("Winner is :", winner)