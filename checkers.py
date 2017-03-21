# The wonderful people who created python made this
import os
# I imported these colors from blender
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    # These are for the checkerboard (I made them myself)
    WHITE = '\033[37m'
    BLACK = '\033[30m'

def display(player, board):
    """Render the board and pieces in pretty colors using ASCII block characters"""
    # Clear the screen
    os.system('clear')
    # Print who's turn it is
    print('Player: ' + str(player) + '\n')
    # These numbers go at the top and are useful in understanding the coordinate output
    print('   0 1 2 3 4 5 6 7')
    # The line at the top
    print('  ----------------')
    # For the numbers going down the left side
    row = 0
    # Print every item of the board
    for i in board:
        print(str(row) + '| ', end='', flush=True)
        for j in i:
            piece = (bcolors.BLACK + '██') if j == 1 else ((bcolors.FAIL + '██') if j == 2 else bcolors.WHITE + '  ')
            print(piece, end='', flush=True)
        #print(bcolors.OKBLUE + '█', end='', flush=True)
        print(bcolors.ENDC, end='', flush=True)
        print(' |')
        row += 1
    print('  ----------------')
def turn(player, board):
    pass
def get_diagonals(piece):
    diagonals = []
    if piece[0] == 0:
        if piece[1] == 0:
            diagonals = [[1,1]]
        elif piece[1] == 7:
            diagonals = [[1,6]]
        else:
            diagonals = [[1,piece[1]+1],[1,piece[1]-1]]
    elif piece[0] == 7:
        if piece[1] == 0:
            diagonals = [[6,1]]
        elif piece[1] == 7:
            diagonals = [[6,6]]
        else:
            diagonals = [[6,piece[1]+1],[6,piece[1]-1]]
    else:
        if piece[1] == 0:
            diagonals = [[piece[0]-1,1],[piece[0]+1,1]]
        elif piece[1] == 7:
            diagonals = [[piece[0]-1,6],[piece[0]+1,6]]
        else:
            diagonals = [[piece[0]+1,piece[1]+1],[piece[0]+1,piece[1]-1],[piece[0]-1,piece[1]+1],[piece[0]-1,piece[1]-1]]
    #print(diagonals)
    return diagonals
def list_moves(player, board):
    pieces = []
    piece = [0,0]
    for i in board:
        piece[1] = 0
        for j in i:
            if j==player or j==player+2:
                current_piece = list(piece)
                #print(current_piece)
                pieces.append(current_piece)
            piece[1] += 1
        piece[0] += 1
    #print(pieces)
    moves = []
    for i in pieces:
        diagonals = get_diagonals(i)
        for j in diagonals:
            if board[j[0]][j[1]] == 0:
                moves.append(list([i, j]))
        #else:
        #    print(str(i) + 'No moves')
    return moves
board = [
[1, 0, 1, 0, 1, 0, 1, 0],
[0, 1, 0, 1, 0, 1, 0, 1],
[1, 0, 1, 0, 1, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 2, 0, 2, 0, 2, 0, 2],
[2, 0, 2, 0, 2, 0, 2, 0],
[0, 2, 0, 2, 0, 2, 0, 2]
]
display(2, board)
for i in list_moves(2, board):
    print(i)
