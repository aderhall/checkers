# The magical python wizards made these
import os
import sys
import time
import copy
import inspect
import random
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
        #print(self.sequence)
        for i in new.sequence:
            #print(i)
            self.sequence.append(i)
            #print(self.sequence)
        return self
    def copy(self, old):
        self.start = old.start
        self.sequence = old.sequence
        self.end = old.end
        return self
    def __str__(self):
        prettypath = ''
        for i in self.sequence:

            prettypath += ', ' + str(i)


        prettypath = prettypath[2:]

        return '* {}Jump{} the piece at {} over {} and finish at {}'.format(bcolors.OKBLUE, bcolors.ENDC, str(self.start), str(prettypath), str(self.end))
    def __repr__(self):
        return '{} through {} to {}'.format(self.start, self.sequence, self.end)
class Move(object):
    """A move"""
    def __init__(self):
        self.start = []
        self.end = []
    def __str__(self):
        return '* {}Move{} the piece at {} to {}'.format(bcolors.OKGREEN, bcolors.ENDC, str(self.start), str(self.end))
    def __repr__(self):
        return '{} to {}'.format(self.start, self.end)
class Path(object):
    """A path of moves."""
    def __init__(self, path):
        self.path = path
        self.persistent = 0
        self.values = self.get_values()
        self.subjective_values = self.get_subjective_values()
        self.depth = self.get_depth()
        self.mean = self.subjective_mean()
        self.stdev = self.subjective_stdev()
    def __str__(self, update=False):
        if update:
            self.update()
        items = len(self.values)
        roots = len(self.path)
        levels = self.depth
        return 'Path of moves containing {} items from {} root moves, extending {} moves ahead.'.format(items, roots, levels)
    def update(self, path=None):
        if path == None:
            pass
        else:
            self.path = path
        self.persistent = 0
        self.values = self.get_values()
        self.subjective_values = self.get_subjective_values()
        self.depth = self.get_depth()
        self.mean = self.subjective_mean()
        self.stdev = self.subjective_stdev()
    def get_values(self, path=None):
        values = []
        if path == None:
            path = self.path
        for i in path:
            if type(path[i]).__name__ == 'dict':
                future = self.get_values(path[i])

                values.extend(future)
            else:
                values.append(path[i])
        return values
    def get_subjective_values(self, path=None):
        valuelist = []
        if path == None:
            path = self.path
        for i in path:
            if type(path[i]).__name__ == 'dict':
                self.persistent += 1
                #print('\t'*(self.persistent-1) + 'Calling self: layer {} on key: {}'.format(self.persistent, i))
                future = self.get_subjective_values(path[i])
                #print('\t'*(self.persistent) + 'Received future values: {}'.format(future))
                valuelist.extend(future)
            else:
                distinction = (1 if self.persistent % 2 == 0 else -1)
                #print('{}: results {}'.format(i, path[i]*distinction))
                valuelist.append(path[i]*distinction)
        self.persistent -= 1
        return valuelist
    def get_depth(self, path=None):
        depth = 0
        if path == None:
            path = self.path
        item = next (iter (path.values()))
        #print(item)
        if type(item).__name__ == 'dict':
            depth += self.get_depth(item)
            depth += 1
        else:
            depth += 1
        return depth
    def subjective_mean(self):
        total = 0
        for i in self.subjective_values:
            total += i if i > 0 else 0
        return total/len(self.values)
    def subjective_stdev(self):
        mean = self.mean
        squares = sum((x-mean)**2 for x in self.subjective_values)
        variance = squares/len(self.values)
        return variance ** .5
    def create_trim(self, path=None, cutoff=None):
        cutoff = 1 if cutoff == None else cutoff
        path = self.path if path == None else path
        trimmed_path = {}
        #path = self.path
        for i in path:
            if type(path[i]).__name__ == 'dict':
                trim = self.create_trim(path[i], cutoff)
                if not trim == None:
                    trimmed_path[i] = trim
            else:

                if (path[i] - self.mean) / self.stdev > cutoff:
                    #print('Results for move: {}  =>  {}'.format(i, path[i]))
                    trimmed_path[i] = path[i]
                    #print(path[i])
                    print('█', end='', flush=True)
        return trimmed_path if len(trimmed_path) > 0 else None
    def trim(self, cutoff=None):
        cutoff = 1 if cutoff == None else cutoff
        newpath = self.create_trim(self.path, cutoff)
        if not newpath == None:
            self.path = newpath
# Define the main functions this program will be using
class Checkers:
    def __init__(self):
        self.arguments = sys.argv
        # RealPlayer style doesn't apply here, I hope :)
        if len(self.arguments) == 1:
            self.realplayer = 1
        elif 'p1' in self.arguments:
            self.realplayer = 1
        elif 'p2' in self.arguments:
            self.realplayer = 2
        self.player = self.realplayer
        # This is the board, prettily drawn out as a '2-dimensional' list of lists

        self.board = [
        [1, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0],
        [0, 1, 0, 2, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 2, 0],
        [0, 0, 0, 2, 0, 2, 0, 0],
        [2, 0, 2, 0, 2, 0, 2, 0],
        [0, 2, 0, 2, 0, 2, 0, 2]
        ]
        # Not a parameter, modified by program. Do not change this, it will mess things up.
        self.recursion_depth = 0
        # Results will be nested a minimum of 2 times, looking at one opposition move after one own move.
        # Subtract 2 from the desired amount and input it into the variable below as a parameter.
        self.recursion_depth_limit = 2
    def display(self, board):
        """Render the board and pieces in pretty colors using ASCII block characters"""
        # Clear the screen
        #os.system('clear')
        # Print who's turn it is
        print('Player: ' + str(self.player) + '\n')
        # These numbers go at the top and are useful in understanding the coordinate output
        print('   0 1 2 3 4 5 6 7')
        # The line at the top
        print('  ------------------')
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
            # Reset the colors and print the border
            print(bcolors.ENDC, end='', flush=True)
            print(' |')
            row += 1
        # Print the bottom border
        print('  ------------------')
    def simmove(self, move, board):
        simboard = []
        for space in board:
            simboard.append(list(space))
        if type(move).__name__ == 'Move':

            simboard[move.start[0]][move.start[1]] = 0
            simboard[move.end[0]][move.end[1]] = self.player
        if type(move).__name__ == 'Jump':

            simboard[move.start[0]][move.start[1]] = 0
            simboard[move.end[0]][move.end[1]] = self.player
            for i in move.sequence:
                simboard[i[0]][i[1]] = 0
        return simboard
    def turn(self, board):
        """Return the decided turn for the player being simulated in the given situation (under construction)"""

        progress = 0
        movecount = 0
        future = {}
        movelist = self.list_moves(board)
        if self.recursion_depth == 0:
            print('Plan Progress (out of {}): '.format(len(movelist)))
        for move in movelist:
            if self.recursion_depth == 0:
                movecount += 1
                newprog = int(10*movecount/len(movelist))
                if newprog > progress:
                    print('█', end='', flush=True)
                    progress += 1

            simboard = self.simmove(move, board)





            if (self.recursion_depth <= self.recursion_depth_limit):

                newboard = self.simmove(move, board)
                self.switch_player()
                self.recursion_depth += 1

                opposition = self.turn(newboard)
                self.switch_player()

                future[move] = opposition
            else:
                distinction = 1

                my_pieces = distinction*len(self.list_pieces(simboard, self.player))
                self.switch_player()

                opponent_pieces = distinction*len(self.list_pieces(simboard, self.player))
                self.switch_player()


                #    print('HohOHOHo')
                future[move] = my_pieces-opponent_pieces



        #    for move in future.keys():

        if self.recursion_depth == 0:
            print('Finished simulating turn: raw path created')
            curframe = inspect.currentframe()
            calframe = inspect.getouterframes(curframe, 2)
            print('Caller name:', calframe[1][3])
        self.recursion_depth -= 1

        return future
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

                        # Get the list of jumps
        # Return the list of possible jumps
        return jumps
    def list_pieces(self, board, player):


        #print(inspect.getouterframes(inspect.currentframe(), 2)[1][3])
        # Assemble list of all of the player's pieces
        # This is a list of all the players pieces
        pieces = []
        # This is the space the function is testing for pieces belonging to the player
        piece = [0,0]
        # Iterate through the rows of the board
        for i in board:

            # Start at the X index of 0 each row (the left side), kind of like a typewriter, if anybody knows what that is
            piece[1] = 0
            # Iterate over every space on the current row
            for j in i:

                # Test if the space is occupied by a piece belonging to the player
                if j==player:
                    # Copy and append the piece coordinates to the list of pieces
                    current_piece = list(piece)
                    pieces.append(current_piece)
                # Move to the next space
                piece[1] += 1
            # Move to the next row
            piece[0] += 1



        return pieces
    def move(self, move):
        board = self.board
        if type(move).__name__ == 'Move':
            board[move.start[0]][move.start[1]] = 0
            board[move.end[0]][move.end[1]] = self.player
        else:
            board[move.start[0]][move.start[1]] = 0
            board[move.end[0]][move.end[1]] = self.player
            for i in move.sequence:
                board[i[0]][i[1]] = 0
    def list_moves(self, board):
        """List all possible moves that the specified player can make in a given situation"""
        pieces = self.list_pieces(board, self.player)
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
    def switch_player(self):
        self.player = 2 if self.player == 1 else 1

# Create the checkers object

checkers = Checkers()

while True:

    plan = None
    print('Displaying')
    # Draw the board
    checkers.display(checkers.board)
    checkers.recursion_depth_limit = 3
    checkers.recursion_depth = 0
    print('Creating Plan')
    plan = Path(checkers.turn(checkers.board))
    original_items = len(plan.values)
    print('\nTrimming Plan')
    plan.trim(2)
    #print(plan.path)
    #print(plan.path)
    print('\nUpdating Plan values')
    plan.update()
    print('Analyzed {} possible situations, eliminated {} of them.'.format(original_items, original_items-len(plan.values)))
    print('Resulting path: {}'.format(plan))
    print('Mean: {}'.format(plan.mean))
    print('Standard Deviation: {}'.format(plan.stdev))
    random_move = random.choice(list(plan.path))
    options = list(plan.path)
    print('Decided on move: {} from list of {} available.'.format(random_move, len(options)))
    time.sleep(1)
    checkers.move(random_move)
    checkers.realplayer = 1 if checkers.realplayer == 2 else 2
    checkers.player = checkers.realplayer

#pathfile = open('assets/0.path', 'w')
#pathfile.write(str(plan.path))
#pathfile.close()


#print(plan)
"""def mean_rank(plan):
    scoresum = 0
    scorecount = 0
    for i in plan:
        if type(plan[i]).__name__ == 'dict':
            future = mean_rank(plan[i])
            scoresum += future[0]
            scorecount += future[1]
        else:

            scoresum += abs(plan[i])
            scorecount += 1
    return list([scoresum, scorecount])
"""
#ranking = mean_rank(plan)
#mean = ranking[0]/ranking[1]
"""
def variance(plan, mean):
    devsum = 0
    devcount = 0
    for i in plan:
        if type(plan[i]).__name__ == 'dict':
            future = variance(plan[i], mean)
            devsum += future[0]
            devcount += future[1]
        else:
            dev = plan[i] - mean
            dev = dev * dev
            devsum += dev
            devcount += 1
    return list([devsum, devcount])
#variance = variance(plan, mean)
#variance = variance[0]/variance[1]
#print(variance)
#stdev = variance ** .5
#print(stdev)
def rank(plan, mean, stdev):
    roadmap = []
    for i in plan:
        if type(plan[i]).__name__ == 'dict':
            roadmap.extend(rank(plan[i], mean, stdev))
        else:
            #print(plan[i])
            if (plan[i] - mean)/stdev > 1:
                roadmap.append(i)
    return roadmap
#ranking = rank(plan, mean, stdev)
#for i in ranking:
#    print('The move: \n {} \nwas selected because its point differential has a Z-score greater than 1'.format(str(i)))
"""
"""
Plan:
go through a dict
if the value is also a dict, call itself for that
if not, test if the abs value is higher than average
if it is higher, add it to a roadmap list
return the roadmap list
"""

"""
for i in plan.keys():
    #print('{}:'.format(i))
    for j in plan[i]:
        #print('\t{}:'.format(j))
        #print('\t\t{}'.format(plan[i][j]))
        for k in plan[i][j]:
            for l in plan[i][j][k]:
                scoresum += abs(plan[i][j][k][l])
                scorecount += 1
average = scoresum/scorecount
print('Average: {}'.format(str(average)))
for i in plan.keys():
    for j in plan[i]:
        for k in plan[i][j]:
            for l in plan[i][j][k]:
                if plan[i][j][k][l] < -2:
                    print('Plan: {} is viable as it got a high score of {}'.format(i, str(plan[i][j][k][l]*-1)))
                    """
""" This is for testing that the non-turn functions work
# Recursively print every move the player can make- side function while turn simulation is not available
print('Moves for player ' + str(checkers.player) + ' (' + ('black' if checkers.player == 1 else 'red') + ')')
print('Coordinates in form (y, x) as shown above')
moves = checkers.list_moves(checkers.board)
for i in moves:
    print(i)
"""
