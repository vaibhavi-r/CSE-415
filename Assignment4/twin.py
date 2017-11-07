import random
import time
from copy import deepcopy
import sys

# START VARIABLES
INITIAL_PLAYER = ''
INITIAL_BOARD = []
INITIAL_BOARD_HASH =''

# PLAYER VARIABLES
MY_NAME = 'Twinnie'
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
    intro = 'I am the Evil Twin'
    return intro

def nickname():
    'Who is this child genius who plays K In A Row?'
    MY_NAME = "Twinnie"
    return  MY_NAME

############################################################
# PREPARE INITIAL LOGIC
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    print("PREPARING")
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
    #init_zobrist()
    #INITIAL_BOARD_HASH = zhash(INITIAL_BOARD)
    #print("Board Hash ", INITIAL_BOARD_HASH)

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

def successors(state):
    'possible next states achievable from current state'
    board = state[0]
    currentPlayer = state[1]

    successorList = []
    for i in range(M):
        for j in range(N):
            if board[i][j] == ' ':
                nextBoard = deepcopy(board)
                nextBoard[i][j] = currentPlayer
                nextPlayer = other(currentPlayer)
                successorList.append([nextBoard, nextPlayer])
    #Possibly order by static val?
    return successorList


def makeMove(currentState, currentRemark, timeLimit=10000):
    move = [0,0]
    currentBoard  = currentState[0]
    whoseTurn = currentState[1]

    if whoseTurn!=MY_SIDE:
        print("What's happening!")

    h = zhash(currentState)


    newState = currentState
    newRemark = utter()
    return [[move, newState], newRemark]
##########################################################################
# MINIMAX RELATED LOGIC

def other(current_player):
    if current_player =='X':
        return 'O'
    elif current_player == 'O':
        return 'X'
    else: print("Error in switching sides")


# MINIMAX with Alpha Beta Pruning
def minimax(state, isMaxPlayer, alpha, beta, depth=0):
    if depth ==0 : #Time ran out
        return staticEval(state)

    nextStates= successors(state)
    if nextStates ==[]:
        return staticEval(state)

    if isMaxPlayer == True:
        bestVal =  -sys.maxsize
        for child in nextStates:
            value = minimax(child,False, alpha, beta,  depth-1)
            bestVal = max(bestVal, value)
            alpha = max(alpha, bestVal)
            if beta <= alpha: #Found a solution
                break
        return bestVal

    else:
        bestVal = -sys.maxsize
        for child in nextStates:
            value = minimax(child,True, alpha, beta, depth-1)
            bestVal = min(bestVal, value)
            beta = min(beta, bestVal)
            if beta <= alpha: #Found a solution
                break
        return bestVal


##########################################################################
# SCORING RELATED LOGIC

STATIC_SCORES={}


def calculate_single_piece_static_evals():
    for r in range(M):
        for c in range(N):
            for piece in range(3):
                h = Z_NUM[r][c]
                piece = PIECE_VAL(INITIAL_BOARD[r][c])  # piece at board[r][c]
                h = h ^ Z_NUM[r * M + c][piece]


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

    score = 0
    # more than 1, 2,.. K-1 in line
    for line in all_lines:
        for k in range(1, K):
            #number in a line
            score += 5^k * line.count('X')
            score -= 5^k * line.count('O')

            #continuous occurrences in a line, needs more than 2
            if k>1:
                score += 10^k * line.count('X'*k)
                score -= 10^k * line.count('O'*k)

    #continuous 1,2,... K-1 in line
    #threats
    #length of line itself
    #Maximum needed for win K

    # Number of available spots in row
    # Whoever is playing gets a basic advantage for same board orientation
    if MY_SIDE ==whoseTurn:
        score += 100

    return score

def flatten(lines):
    'Reduce a list of lines to single strings for each row/column/diagonal'
    flat_lines = []
    for line in lines:
        new_line = ''.join(piece if piece != '' else '*' for piece in line)
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