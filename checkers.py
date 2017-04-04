# The wonderful people who created python made these
import os
import sys
import time

# I copied these colors from blender
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
# Check if the user has specified a specific player
class Jump(object):
    """A jump sequence"""
    def __init__(self):
        self.start = []
        self.sequence = []
        self.end = []
    def append(self, new):

        self.end = new.end
        for i in new.sequence:
            self.sequence.append(i)
        return self
    def copy(self, old):
        self.start = old.start
        self.sequence = old.sequence
        self.end = old.end
        return self
    def __str__(self):
        return '* {}Jump{} the piece at {} over {} and finish at {}'.format(bcolors.OKBLUE, bcolors.ENDC, str(self.start), str(self.sequence), str(self.end))
class Move(object):
    """A move"""
    def __init__(self):
        self.start = []
        self.end = []
    def __str__(self):
        return '* {}Move{} the piece at {} to {}'.format(bcolors.OKGREEN, bcolors.ENDC, str(self.start), str(self.end))

# Define the main functions this program will be using
class Checkers:
    def __init__(self):
        self.arguments = sys.argv
        if len(self.arguments) == 1:
            self.player = 1
        elif 'p1' in self.arguments:
            self.player = 1
        elif 'p2' in self.arguments:
            self.player = 2
        # This is the board, prettily drawn out as a '2-dimensional' list of lists

        self.board = [
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 2, 0, 2, 0, 2],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2]
        ]
    def display(self):
        """Render the board and pieces in pretty colors using ASCII block characters"""
        # Clear the screen
        os.system('clear')
        # Print who's turn it is
        print('Player: ' + str(self.player) + '\n')
        # These numbers go at the top and are useful in understanding the coordinate output
        print('   0 1 2 3 4 5 6 7')
        # The line at the top
        print('  ------------------')
        # For the numbers going down the left side
        row = 0
        # Print every item of the board
        for i in self.board:
            # Print the row index and border
            print(str(row) + '| ', end='', flush=True)
            # Print the pieces
            for j in i:
                # Set the actual piece to a 2-char block character of the appropriate color
                piece = (bcolors.BLACK + '██') if j == 1 else ((bcolors.FAIL + '██') if j == 2 else bcolors.WHITE + '  ')
                # Print it
                print(piece, end='', flush=True)
            # Reset the colors and print the border
            print(bcolors.ENDC, end='', flush=True)
            print(' |')
            row += 1
        # Print the bottom border
        print('  ------------------')
    def turn(self):
        """Return the decided turn for the player being simulated in the given situation (under construction)"""
        pass
    def get_diagonals(self, piece):
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

        # Return the list of lists ( [[coordinate1Y, coordinate1X], [coordinate2Y, coordinate2X]...] )
        return diagonals
    def get_player(self, piece):
        """Get the player who controls a given piece"""
        return self.board[piece[0]][piece[1]]
    def is_opponent(self, piece):
        """Test if a given piece is the opponent of a player"""
        test = self.get_player(piece)
        if test == self.player + 3 or test == self.player + 1 or test == self.player -3 or test == self.player -1:
            return True
        else:
            return False
    def is_open(self, home, piece):
        """Test if a piece is open for jumps from a 'home' piece"""
        if abs(home[0]-piece[0]) == 2 and abs(home[1]-piece[1]) == 2 and self.get_player(piece) == 0:
            return True
        else:
            return False
    def get_jumps(self, piece, board):
        """Get the jump moves possible for a piece on the board"""
        # Jumps will be put in this list
        jumps = []
        # Test in which direction it should be going
        if self.player == 2:
            direction = -1
        else:
            direction = 1
        # Get all diagonal spaces of the piece
        diagonals = self.get_diagonals(piece)
        # Iterate over the diagonals
        for i in diagonals:
            # Test if the space is occupied by an opponent and is in front of the piece
            if piece[0] + direction == i[0] and self.is_opponent(i) and (not self.get_player(i) == 0):
                # Get all diagonal spaces of the opponent's piece
                destinations = self.get_diagonals(i)
                # Iterate over these diagonals
                for j in destinations:
                    # Test if the piece is open for jumps
                    if self.is_open(piece, j):
                        # If so, add it to the list
                        # Create a simulated board
                        simboard = []
                        # Add each row to the list
                        for space in board:
                            simboard.append(list(space))
                        # Remove the piece in the middle of the jump
                        # Clear the space that was left
                        simboard[piece[0]][piece[1]] = 0
                        simboard[i[0]][i[1]] = 0
                        # Set the target space to an occupied space
                        simboard[j[0]][j[1]] = self.player
                        # The original jump
                        jump = Jump()
                        jump.start = piece
                        jump.sequence.append(i)
                        jump.end = j
                        futurejumps = self.get_jumps(j, simboard)
                        future = False
                        for f in futurejumps:
                            newjump = Jump()
                            newjump.copy(jump)
                            jumps.append(newjump.append(f))
                            future = True
                        if not future:
                            jumps.append(jump)
                        return jumps
                        # Get the list of jumps
        # Return the list of possible jumps
        return jumps
    def list_moves(self, board):
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
                if j==self.player or j==self.player+2:
                    # Copy and append the piece coordinates to the list of pieces
                    current_piece = list(piece)
                    pieces.append(current_piece)
                # Move to the next space
                piece[1] += 1
            # Move to the next row
            piece[0] += 1
        # Calculate moves each piece can make
        # This is a list of all moves each piece can make
        moves = []
        # Iterate over the newly made list of pieces
        for i in pieces:
            # Get the diagonal spaces surrounding the piece
            diagonals = self.get_diagonals(i)
            # Iterate over the diagonals and check for availability
            for j in diagonals:
                if board[j[0]][j[1]] == 0 and j[0] == i[0] + (1 if self.player == 1 else -1):
                    # If this is a valid move, add it to the list
                    # Create a move object and set its properties
                    move = Move()
                    move.start = i
                    move.end = j
                    # Add it to the list
                    moves.append(move)
            # Get all possible jumps for the piece
            jumps = self.get_jumps(i, board)
            # Add each one to the list
            for j in jumps:
                moves.append(j)
        # Return the list
        return moves

# Create the checkers object

checkers = Checkers()

# Draw the board
checkers.display()

# Recursively print every move the player can make- side function while turn simulation is not available
print('Moves for player ' + str(checkers.player) + ' (' + ('black' if checkers.player == 1 else 'red') + ')')
print('Coordinates in form (y, x) as shown above')
moves = checkers.list_moves(checkers.board)
for i in moves:
    print(i)
