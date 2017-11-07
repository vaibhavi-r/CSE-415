import random

# START VARIABLES
INITIAL_PLAYER = ''
INITIAL_BOARD = []
INITIAL_BOARD_HASH =''

# PLAYER VARIABLES
MY_NAME = 'Madeline'
MY_SIDE = ''
OPP_NAME = ''
OPP_SIDE = ''

# GAME PARAMETERS
M = 0
N = 0
K = 0

# STATE EVAL VARIABLES
NUM_AVAILABLE_SPOTS = 0
NUM_FORBIDDEN_SPOTS = 0
NUM_FILLED_SPOTS = 0
NUM_X = 0
NUM_O = 0

OPEN_SPOTS = []
############################################################
# INTRODUCTION
def introduce():
    intro = 'In an old house in Paris that was covered in vines\n'+\
            'lived twelve little girls in two straight lines.\n' +\
            'And I am a one of them, they call me, Madeline\n' +\
            'Vaibhavi (vaibhavi@uw.edu) is a teacher of mine\n' +\
            'I learnt K-In-A-Row from her by River Seine\n' +\
            'Now let us play, thanks to artificial design!\n'
    return intro

def nickname():
    'Who is this child genius who plays K In A Row?'
    return 'Madeline'

############################################################
# PREPARE INITIAL LOGIC
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    INITIAL_BOARD = initial_state[0]
    INITIAL_PLAYER = initial_state[1]

    M = len(initial_state[0])
    N = len(initial_state[0][0])
    K = k

    MY_SIDE = what_side_I_play
    if what_side_I_play == 'X': OPP_SIDE='O'
    else: OPP_SIDE = 'X'

    OPP_NAME = opponent_nickname

    #Zobrist Hashing
    init_zobrist()
    INITIAL_BOARD_HASH = hash(INITIAL_BOARD)
    print("Board Hash ", INITIAL_BOARD_HASH)

    return "OK"

def parse_initial_board():
    global NUM_O, NUM_X, NUM_FORBIDDEN_SPOTS, NUM_FILLED_SPOTS, NUM_AVAILABLE_SPOTS
    global M,N

    for i in range(M):
        for j in range(N):
            tile = INITIAL_BOARD[i][j]
            if tile == '':
                NUM_AVAILABLE_SPOTS += 1
            elif tile == 'X':
                NUM_X +=1
                NUM_FILLED_SPOTS +=1
            elif tile == 'O':
                NUM_O += 1
                NUM_FILLED_SPOTS +=1
            else:
                NUM_FORBIDDEN_SPOTS += 1

    print()
############################################################
# ZOBRIST HASHING

PIECE_VAL = {'O':0, 'X':1, '-':2 , '':3}
Z_NUM =[]  #2d array of size (MxN) by 4 (positions x pieces)
Z_SCORES ={} #State Evals stored with iteration depth

def init_zobrist():
# fill Z table with random numbers/bitstrings
    print("Initializing Zobrist Table for Board Size:",M,'by',N)
    for tile in range(M*N):  # loop over the board as a linear array
        Z_NUM[tile] = []
        for piece in range(4):  # loop over the pieces
            Z_NUM[tile][piece] = random.getrandbits(10)

def zhash(board):
    h=0
    for r in range(M):
        for c in range(N):
            if board[r][c] != '':
                piece = PIECE_VAL(board[r][c]) #piece at board[r][c]
                h = h^Z_NUM[r*M+c][piece]
    return h


def update_Z_SCORE(h, score, depth=0):
    if h not in Z_SCORES:
        Z_SCORES[h] = [score,0]
    else:
        Z_SCORES[h] = [score,depth]

############################################################
# MOVE MAKING LOGIC
def makeMove(currentState, currentRemark, timeLimit=10000):
    move = [0,0]
    currentBoard  = currentState[0]
    whoseTurn = currentState[1]

    if whoseTurn!=MY_SIDE:
        print("What's happening!")

    h = hash(currentState)


    newState = currentState
    newRemark = utter()
    return [[move, newState], newRemark]

############################################################
# MINIMAX
'''
def minimax(node, depth, isMaximizingPlayer, alpha, beta):
    if node is a leaf node:
        return value
        of
        the
        node

    if isMaximizingPlayer:
        bestVal = -INFINITY
        for each child node:
            value = minimax(node, depth + 1, false, alpha, beta)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha:
                break
        return bestVal

    else:
        bestVal = +INFINITY
        for each child node:
            value = minimax(node, depth + 1, true, alpha, beta)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha:
                break
        return bestVal
'''

#Iterative Deepening

##########################################################################
# STATE RELATED LOGIC

STATIC_SCORES={}


def calculate_single_piece_static_evals():
    for r in range(M):
        for c in range(N):
            for piece in range(3):
                h = Z_NUM[r][c]
                piece = PIECE_VAL(INITIAL_BOARD[r][c])  # piece at board[r][c]
                h = h ^ Z_NUM[r * M + c][piece]


def create_board():
    global INITIAL_BOARD
    print(INITIAL_BOARD)
    return []

def staticEval(state):
    board = state[0]
    whoseTurn = state[1]

    rows = []
    cols = []
    diags1 = []
    diags2 = []

    #Find number of rows with K in a row
    for i in range(M):
        rows.append(board[i])
        for j in range(N):
            piece = board[i][j]
            cols[j].append(piece)
            diags1[M-1+i].append(piece)

    all_lines = []

    flat_rows = flatten(rows)
    flat_cols = flatten(cols)
    flat_diags1 = flatten(diags1)
    flat_diags2 = flatten(diags2)

    all_lines.extend(flat_rows)
    all_lines.extend(flat_cols)
    all_lines.extend(flat_diags1)
    all_lines.extend(flat_diags2)

    # Number of rows with 1  X
    # Number of rows with 2  X
    # Number of rows with K  X

    # Number of rows with 1  X
    # Number of rows with 2  X

    score = 0

    return score

def flatten(lines):
    'Reduce a list of lines to single strings for each row/column/diagonal'

    flat_lines = []
    for line in lines:
        new_line = ''.join(piece if piece !='' else '*' for piece in line)

    flat_lines.append(new_line)

    return flat_lines
##########################################################################
# CONVERSATIONAL LOGIC
def utter():
    return "Aha"

"""
lose, win, game, play, player, loser, winner, tough, easy, puzzle, move, go, stop, start, finish, close
saved game, blocked you
"""

def respond(currentState, currentRemark):
    return "Aha"

##########################################################################