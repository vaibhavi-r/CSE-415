'''TowersOfHanoi.py
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
PROBLEM_NAME = "Basic Eight Puzzle"
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
                print("Invalud Directions")
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

# </COMMON_CODE>



# <COMMON_DATA>
N_tiles = 9
TILES_LIST = range(0,N_tiles)
# </COMMON_DATA>


# <INITIAL_STATE>

# puzzle0:
#CREATE_INITIAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])

# puzzle1a:
#CREATE_INITIAL_STATE = lambda: State([1, 0, 2, 3, 4, 5, 6, 7, 8])

# puzzle2a:
#CREATE_INITIAL_STATE = lambda: State([3, 1, 2, 4, 0, 5, 6, 7, 8])

# puzzle4a:
CREATE_INITIAL_STATE = lambda: State([1, 4, 2, 3, 7, 0, 6, 8, 5])

#INITIAL_LIST = [0,1,2,3,4,5,6,7,8]
#CREATE_INITIAL_STATE = lambda: State(INITIAL_LIST)

CREATE_GOAL_STATE = lambda: State([0, 1, 2, 3, 4, 5, 6, 7, 8])
# DUMMY_STATE =  [0,1,2,3,4,5,6,7,8]

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
