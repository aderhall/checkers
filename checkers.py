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
            if board[j[0]][j[1]] == 0:
                # If this is a valid move, add it to the list
                moves.append(list([i, j]))
        #else:
        #    print(str(i) + 'No moves')
    # Return the list
    return moves
# This is the board, prettily drawn out as a '2-dimensional' list of lists
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
# Draw the board
display(2, board)
# Recursively print every move the player can make
for i in list_moves(2, board):
    print(i)
