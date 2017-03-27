# The wonderful people who created python made this
import os
import sys
arguments = sys.argv
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
if len(arguments) == 1:
    player = 1
elif 'p1' in arguments:
    player = 1
elif 'p2' in arguments:
    player = 2
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
        # Print the row index and border
        print(str(row) + '| ', end='', flush=True)
        # Print the pieces
        for j in i:
            # Set the actual piece to a 2-char block character of the appropriate color
            piece = (bcolors.BLACK + '██') if j == 1 else ((bcolors.FAIL + '██') if j == 2 else bcolors.WHITE + '  ')
            # Print it
            print(piece, end='', flush=True)
        #print(bcolors.OKBLUE + '█', end='', flush=True)
        # Reset the colors and print the border
        print(bcolors.ENDC, end='', flush=True)
        print(' |')
        row += 1
    # Print the bottom border
    print('  ----------------')
def turn(player, board):
    """Return the decided turn for the player being simulated in the given situation"""
    pass
def get_diagonals(piece):
    """Get the diagonal spaces around a space and return a list of lists containing their coordinates"""
    # Test if the piece is against an edge of the board; if so, get the coordinates that apply
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
            # If the piece is not against an edge, calculate diagonals with a formula
            diagonals = [[piece[0]+1,piece[1]+1],[piece[0]+1,piece[1]-1],[piece[0]-1,piece[1]+1],[piece[0]-1,piece[1]-1]]
    #print(diagonals)
    # Return the list of lists ( [[coordinate1Y, coordinate1X], [coordinate2Y, coordinate2X]...] )
    return diagonals
def get_player(piece, board):
    return board[piece[0]][piece[1]]
def is_opponent(piece, board, player):
    test = get_player(piece, board)
    if test == player + 3 or test == player + 1 or test == player -3 or test == player -1:
        return True
    else:
        return False
def is_open(home, piece, board):
    if abs(home[0]-piece[0]) == 2 and abs(home[1]-piece[1]) == 2:
        return True
    else:
        return False
"""def get_jumps(piece, board):
    player = get_player(piece, board)
    diagonals = get_diagonals(piece)
    jumps = []
    for i in diagonals:
        #print(diagonals)
        if is_opponent(i, board, player):
            spaces = get_diagonals(i)
            for j in spaces:
                if is_open(piece, j, board) and (j[0]<piece[0]):
                    jumps.append(list([piece, j]))
    print(jumps)
    if not len(jumps) == 0:
        for i in jumps:
            jumps.append(get_jumps(i[1], board))

    return jumps
"""
def get_jumps(piece, board, player):
    jumps = []
    if player == 2:
        direction = -1
    else:
        direction = 1
    diagonals = get_diagonals(piece)
    #print('Diagonals for piece ' + str(piece) + ': ' + str(diagonals))
    for i in diagonals:
        #print('Testing piece ' + str(i))
        if piece[0] + direction == i[0] and is_opponent(i, board, player):
            destinations = get_diagonals(i)
            #print('Destinations for piece ' + str(i) + ': ' + str(destinations))
            for j in destinations:
                #print('Testing piece ' + str(j))
                if is_open(piece, j, board):
                    jumps.append(list([piece, j]))
    return jumps
def list_moves(player, board):
    """List all possible moves that the specified player can make in a given situation"""
    # Assemble list of all of the player's pieces
    # This is a list of all the players pieces
    pieces = []
    # This is the space the function is testing for pieces belonging to the player
    piece = [0,0]
    # Iterate through the rows of the board
    for i in board:
        # Start at the X index of 0 each row (the left side, like a typewriter, if anybody knows what that is)
        piece[1] = 0
        # Iterate over every space on the current row
        for j in i:
            # Test if the space is occupied by a piece belonging to the player
            if j==player or j==player+2:
                # Copy and append the piece coordinates to the list of pieces
                current_piece = list(piece)
                #print(current_piece)
                pieces.append(current_piece)
            # Move to the next space
            piece[1] += 1
        # Move to the next row
        piece[0] += 1
    #print(pieces)
    # Calculate moves each piece can make
    # This is a list of all moves each piece can make
    moves = []
    # Iterate over the newly made list of pieces
    for i in pieces:
        # Get the diagonal spaces surrounding the piece
        diagonals = get_diagonals(i)
        # Iterate over the diagonals and check for availability
        for j in diagonals:
            if board[j[0]][j[1]] == 0 and j[0] == i[0] + (1 if player == 1 else -1):
                # If this is a valid move, add it to the list
                moves.append(list([i, j]))
        jumps = get_jumps(i, board, player)
        for j in jumps:
            moves.append(j)
        #else:
        #    print(str(i) + 'No moves')
    # Return the list
    return moves
# This is the board, prettily drawn out as a '2-dimensional' list of lists
board = [
[1, 0, 1, 0, 1, 0, 1, 0],
[0, 1, 0, 1, 0, 1, 0, 1],
[1, 0, 1, 0, 0, 0, 1, 0],
[0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 1, 0, 1, 0, 0, 0],
[0, 2, 0, 2, 0, 2, 0, 2],
[2, 0, 2, 0, 2, 0, 2, 0],
[0, 2, 0, 2, 0, 2, 0, 2]
]
# Draw the board
display(player, board)
# Recursively print every move the player can make
print('Moves for player ' + str(player) + ' (' + ('black' if player == 1 else 'red') + ')')
print('Coordinates in form (y, x) as shown above')
for i in list_moves(player, board):
    #print(i)
    print('Move piece ' + (str(i[0]).replace('[', '(')).replace(']', ')') + ' to ' + (str(i[1]).replace('[', '(')).replace(']', ')'))
