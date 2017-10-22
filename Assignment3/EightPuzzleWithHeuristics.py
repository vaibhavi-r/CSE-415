'''
Name    = Vaibhavi Rangarajan
UWNetID = vaibhavi

EightPuzzle with Heuristics.py
A QUIET2 Solving Tool problem formulation.
QUIET = Quetzal User Intelligence Enhancing Technology.
The XML-like tags used here serve to identify key sections of this
problem formulation.  It is important that COMMON_CODE come
before all the other sections (except METADATA), including COMMON_DATA.
CAPITALIZED constructs are generally present in any problem
formulation and therefore need to be spelled exactly the way they are.
Other globals begin with a capital letter but otherwise are lower
case or camel case.
'''
# <METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Eight Puzzle With Heuristics"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['Vaibhavi Rangarajan']
PROBLEM_CREATION_DATE = "17-OCT-2017"
PROBLEM_DESC = \
    '''This formulation of the Basic Eight Puzzle problem uses generic
    Python 3 constructs and has been tested with Python 3.6.
    It is designed to work according to the QUIET2 tools interface.
    '''

# </METADATA>

# <COMMON_CODE>
class State:
    def __init__(self, d):
        self.d = d

    def __eq__(self, s2):
        for tile in TILES_LIST:
            if self.d[tile] != s2.d[tile]: return False
        return True

    def __str__(self):
        # Produces a textual description of a state.
        # Might not be needed in normal operation with GUIs.
        txt = "["
        for tile in TILES_LIST:
            txt+= str(self.d[tile])+ " ,"

        return txt[:-2] + "]"

    def __hash__(self):
        return (self.__str__()).__hash__()

    def copy(self):
        # Performs an appropriately deep copy of a state,
        # for use by operators in creating new states.
        news = State([])

        for tile in TILES_LIST:
            news.d.append(self.d[tile])

        return news


    def can_move(self, direction):
        '''Tests whether it's legal to move a tile from board in state s
           in the given direction to fill the blank space.'''
        try:
            if self.d == []:
                return False    #No tiles placed anywhere, empty board

            blank_idx = self.d.index(0)  # Find where blank tile is
#            print("CAN MOVE?\n-------")
#            print("0 is at index ", blank_idx)
#            print("Moving in direction ", direction)

            # Find which tile to move
            if direction == "RIGHT":
                blank_offset = -1
            elif direction == "LEFT":
                blank_offset = +1
            elif direction == "DOWN":
                blank_offset = -3
            elif direction == "UP":
                blank_offset = +3
            else:
                print("Invalid Directions")
                return False # Invalid direction

            # index of tile to swap
            tile_idx = blank_idx + blank_offset
            if tile_idx in TILES_LIST:
                return True             # Valid tile to swap with blank
            else:
                return False          # Invalid tile

        except (Exception) as e:
            print(e)

    def move(self, direction):
        '''Assuming it's legal to make the move, this computes
           the new state resulting from moving the topmost disk
           from the From peg to the To peg.'''

#        print("MOVE\n-------")
#        print("MOVE to ", direction)
#        print("0 is at index ", blank_idx)

        news = self.copy()  # start with a deep copy.
        blank_idx = self.d.index(0) #Find where blank tile is


        #Find which tile to move
        blank_offset = 0
        if direction == "RIGHT":
            blank_offset= -1
        elif direction == "LEFT":
            blank_offset = +1
        elif direction == "DOWN":
            blank_offset = -3
        elif direction == "UP":
            blank_offset= +3

        tile_idx = blank_idx + blank_offset

        # swap the tile to move with blank space
        news.d[blank_idx], news.d[tile_idx] = self.d[tile_idx], self.d[blank_idx]

        return news  # return new state


def goal_test(s):
    '''If the number 0 is in tile0, 1 is in tile 1, and so forth unti 8 is in tile8, then s is a goal state.'''
    for t in TILES_LIST:
        if s.d[t] != t: return False
    return True

def goal_message(s):
    return "The Eight Tiles Are Aligned!"

class Operator:
    def __init__(self, name, precond, state_transf):
        self.name = name
        self.precond = precond
        self.state_transf = state_transf

    def is_applicable(self, s):
        return self.precond(s)

    def apply(self, s):
        return self.state_transf(s)


h_euclidean = lambda S: euclidean_dist(S)
h_hamming   = lambda S: hamming_dist(S)
h_manhattan = lambda S: manhattan_dist(S)
h_custom    = lambda S: linear_conflict_dist(S)

def euclidean_dist(S):
    if goal_test(S):
        return 0
    else:
        import math
        dist = 0
        for t in TILES_LIST:
            curr = S.d[t]
            x1,y1 = translate_x_y(curr) #current position of given tile in x-y coordinates
            x2,y2 = translate_x_y(t)    #goal position of given tile in x-y coordinates
            dist += math.sqrt((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2))   #Euclidean Distance
        return dist

def hamming_dist(S):
    if goal_test(S):
        return 0
    else:
        dist = 0
        for t in TILES_LIST:
            if S.d[t] !=t:
                dist+=1
        return dist


def manhattan_dist(S):
    if goal_test(S):
        return 0
    else:
        dist =0
        for t in TILES_LIST:
            curr = S.d[t]
            x1,y1 = translate_x_y(curr) #current position of given tile in x-y coordinates
            x2,y2 = translate_x_y(t)    #goal position of given tile in x-y coordinates

            dist += abs(x1-x2)  #Horizontal difference
            dist += abs(y1-y2)  #Vertical difference
        return dist

def translate_x_y(num):
    if num==0:
        return 0,0

    y = num//3
    x = num%3
    return x,y

def linear_conflict_dist(S):
    '''Idea for custom linear conflict distance was refined
    by using https: // heuristicswiki.wikispaces.com / N + -+Puzzle

    For every linear conflict found where 2 tiles need to cross each other in same line,
    to get to their end position, add 2 to manhattan distance
    '''

    if goal_test(S):
        return 0
    else:
        #Calculate Manhattan distance for whole board
        m_dist=manhattan_dist(S)

        #Calculate extra offsets for linear conflicts
        lc_offset = 0

        #Rows
        for row in range(0,3):
            ideal_row = TILES_LIST[3*row:(3*row)+3]
            curr_row = S.d[3*row : (3*row)+3]

            common = [x for x in ideal_row if x in curr_row]
            common_conflicts = [c for c in common if ideal_row.index(c) != curr_row.index(c)]

            if common_conflicts==[] or len(common_conflicts)==1: #No possible conflicting pairs
                continue

            if len(common_conflicts)==2:
                i,j = common_conflicts[0], common_conflicts[1]
                if ideal_row.index(i) < ideal_row.index(j) and curr_row.index(i) > curr_row.index(j):
                    lc_offset+=2

            elif len(common_conflicts) ==3:
                i,j,k = common_conflicts[0], common_conflicts[1], common_conflicts[2]

                if ideal_row.index(i) < ideal_row.index(j) and curr_row.index(i) > curr_row.index(j):
                    lc_offset+=2

                if ideal_row.index(j) < ideal_row.index(k) and curr_row.index(j) > curr_row.index(k):
                    lc_offset += 2

                if ideal_row.index(k) < ideal_row.index(i) and curr_row.index(k) > curr_row.index(i):
                    lc_offset += 2

        #Columns
        ideal_columns = [[],[],[]]
        curr_columns = [[],[],[]]

        for idx in range(0,9):
            ideal_columns[idx//3].append(TILES_LIST[idx])
            curr_columns[idx//3].append(S.d[idx])

        for col in range(0,3):
            ideal_col = ideal_columns[col]
            curr_col = curr_columns[col]

            common = [x for x in ideal_col if x in curr_col]  #Elements that are in their correct column
            common_conflicts = [c for c in common if ideal_col.index(c) != curr_col.index(c)] #Elements that are in correct column, but not correct position

            if common_conflicts == [] or len(common_conflicts) == 1:  # No possible conflicting pairs
                continue

            if len(common_conflicts) == 2:
                i, j = common_conflicts[0], common_conflicts[1]
                if ideal_col.index(i) < ideal_col.index(j) and curr_col.index(i) > curr_col.index(j):
                    lc_offset += 2

            elif len(common_conflicts) == 3:
                i, j, k = common_conflicts[0], common_conflicts[1], common_conflicts[2]

                if ideal_col.index(i) < ideal_col.index(j) and curr_col.index(i) > curr_col.index(j):
                    lc_offset += 2

                if ideal_col.index(j) < ideal_col.index(k) and curr_col.index(j) > curr_col.index(k):
                    lc_offset += 2

                if ideal_col.index(k) < ideal_col.index(i) and curr_col.index(k) > curr_col.index(i):
                    lc_offset += 2


        return lc_offset + m_dist



HEURISTICS = {'h_euclidean': h_euclidean, 'h_hamming': h_hamming,
              'h_manhattan': h_manhattan, 'h_custom': h_custom}
# </COMMON_CODE>


# <COMMON_DATA>
N_tiles = 9
TILES_LIST = range(0,N_tiles)
# </COMMON_DATA>


# <INITIAL_STATE>

# puzzle0:
#CREATE_INITIAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])

# puzzle1a:
CREATE_INITIAL_STATE = lambda: State([1, 0, 2, 3, 4, 5, 6, 7, 8])

# puzzle2a:
#CREATE_INITIAL_STATE = lambda: State([3, 1, 2, 4, 0, 5, 6, 7, 8])

# puzzle4a:
#CREATE_INITIAL_STATE = lambda: State([1, 4, 2, 3, 7, 0, 6, 8, 5])

#INITIAL_LIST = [0,1,2,3,4,5,6,7,8]
#CREATE_INITIAL_STATE = lambda: State(INITIAL_LIST)

CREATE_GOAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])
# DUMMY_LIST =  [0,1,2,3,4,5,6,7,8]

# </INITIAL_STATE>

# <OPERATORS>

possible_directions = ["LEFT", "RIGHT", "DOWN", "UP"]

OPERATORS = [Operator("Move a tile towards - " + dir,
                      lambda s, direction = dir: s.can_move(direction),
                      lambda s, direction = dir: s.move(direction))
             for dir in possible_directions]


# <GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
# </GOAL_TEST>

# <GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
# </GOAL_MESSAGE_FUNCTION>

# <STATE_VIS>
if 'BRYTHON' in globals():
    from TowersOfHanoiVisForBrython import set_up_gui as set_up_user_interface
    from TowersOfHanoiVisForBrython import render_state_svg_graphics as render_state
    # if 'TKINTER' in globals(): from TicTacToeVisForTKINTER import set_up_gui
    # </STATE_VIS>




