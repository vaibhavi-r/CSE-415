import random
import time
from copy import deepcopy
import sys

# START VARIABLES
INITIAL_PLAYER = ''
INITIAL_BOARD = []
INITIAL_BOARD_HASH =''


# PLAYER VARIABLES
MY_NAME = ''
MY_SIDE = ''
OPP_NAME = ''
OPP_SIDE = ''

# GAME PARAMETERS
M = 0
N = 0
K = 0
TIME_LIMIT =0

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
    intro = '\nIn an old house in Paris that was covered in vines\n'+\
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
    global M,N,K
    global INITIAL_BOARD, INITIAL_PLAYER
    global MY_SIDE, MY_NAME, OPP_SIDE, OPP_NAME

    print("PREPARING")
    INITIAL_BOARD = initial_state[0]
    INITIAL_PLAYER = initial_state[1]

    M = len(initial_state[0])
    N = len(initial_state[0][0])
    K = k

    MY_SIDE = what_side_I_play
    print('My side', MY_SIDE)
    if what_side_I_play == 'X': OPP_SIDE='O'
    else: OPP_SIDE = 'X'

    OPP_NAME = opponent_nickname
    MY_NAME = nickname()


    #Zobrist Hashing
    init_zobrist()

    #INITIAL_BOARD_HASH = zhash(INITIAL_BOARD)
    #print("Board Hash ", INITIAL_BOARD_HASH)

    parse_initial_board()

    return "OK"

def parse_initial_board():
    global NUM_O, NUM_X, NUM_FORBIDDEN_SPOTS, NUM_FILLED_SPOTS, NUM_AVAILABLE_SPOTS
    global M,N
    global OPEN_SPOTS

    for i in range(M):
        for j in range(N):
            tile = INITIAL_BOARD[i][j]
            if tile == ' ':
                NUM_AVAILABLE_SPOTS += 1
                OPEN_SPOTS.append([i,j])
            elif tile == 'X':
                NUM_X +=1
                NUM_FILLED_SPOTS +=1
            elif tile == 'O':
                NUM_O += 1
                NUM_FILLED_SPOTS +=1
            else:
                NUM_FORBIDDEN_SPOTS += 1

    print("OPEN SPOTS", OPEN_SPOTS)


############################################################
# ZOBRIST HASHING

PIECE_VAL = {'O':1, 'X':2} #, '-':3 , ' ':4}
Z_NUM =[]  #2d array of size (MxN) by 2 (positions x pieces)
Z_SCORES ={} #Static State Evals stored without iteration depth

def init_zobrist():
    global M, N
    global Z_NUM
    global Z_SCORES

    Z_SCORES = {}

    # fill Z table with random numbers/bitstrings
    print("Initializing Zobrist Table for Board Size:",M,'by',N)
    for tile in range(M*N):  # loop over the board as a linear array
        Z_NUM.append([[],[]])
        for piece in range(2):  # loop over the pieces
            Z_NUM[tile][piece] = random.getrandbits(32)

def zhash(board):
    global Z_NUM, M, N
    h=0
    print('zhash--')
    for r in range(M):
        for c in range(N):
            if board[r][c] != ' ' and board[r][c] != '-':
                print("Found piece:", board[r][c])
                piece = PIECE_VAL[board[r][c]] #piece at board[r][c]
                h = h^Z_NUM[r*M+c][piece]
    return str(h)

############################################################
# MOVE MAKING LOGIC

def successors(state):
    global M, N, NUM_AVAILABLE_SPOTS, OPEN_SPOTS
    'possible next states achievable from current state'
    board = state[0]
    currentPlayer = state[1]
    successorList = []

    for spot in OPEN_SPOTS:
        [i,j] = spot
        if board[i][j] == ' ':
            nextBoard = deepcopy(board)
            nextBoard[i][j] = currentPlayer
            nextPlayer = other(currentPlayer)
            successorList.append([nextBoard, nextPlayer])
        else:
            OPEN_SPOTS.remove(spot)
            NUM_AVAILABLE_SPOTS -=1

        #    for i in range(M):
#        for j in range(N):

    #Possibly order by static val?
    #print("Successors = ", len(successorList))
    return successorList

def makeMove(currentState, currentRemark, timeLimit=10000):
    global OPEN_SPOTS, MY_SIDE, TIME_LIMIT, NUM_AVAILABLE_SPOTS
    now = time.time()
    TIME_LIMIT = timeLimit


    currentBoard  = currentState[0]
    whoseTurn = currentState[1]

    if whoseTurn!=MY_SIDE:
        print("What's happening!")

    init_alpha = -sys.maxsize
    init_beta  = sys.maxsize
    init_depth = 2

    newState = minimax(currentState, isMaxPlayer=True, startTime=now, alpha=init_alpha, beta=init_beta, depth=init_depth)

    move = getMove(currentState, newState)
    print("MOVE", move)

    OPEN_SPOTS.remove(move)
    NUM_AVAILABLE_SPOTS -= 1

    newRemark = respond(newState,currentRemark)

    return [[move, newState], newRemark]


def getMove(state, newState):
    board = state[0]
    newBoard = newState[0]

    #expect only one row will change
    for spot in OPEN_SPOTS:
        i = spot[0]
        j = spot[1]
        if board[i][j] !=newBoard[i][j]:
            return [i,j]

    return None

##########################################################################
# MINIMAX RELATED LOGIC

def other(current_player):
    if current_player =='X':
        return 'O'
    elif current_player == 'O':
        return 'X'
    else: print("Error in switching sides")


# MINIMAX with Alpha Beta Pruning
def minimax(state, isMaxPlayer, startTime, alpha, beta, depth=0):
#    if depth<=0: #Time ran out
#        print("No more depth")
#        return state

    if TIME_LIMIT - (time.time() - startTime) <  0.15:
        #print("Timeout")
        return state

    nextStates= successors(state)
    if nextStates ==[]:
        return state


    if isMaxPlayer == True:
        bestVal =  -sys.maxsize
        for child in nextStates:
            new_state = minimax(child, False, startTime, alpha, beta,  depth+1)
            bestVal = max(bestVal, get_static_score(new_state))
            alpha = max(alpha, bestVal)
            if beta <= alpha: #Found a solution
                break
        return child

    else:
        bestVal = -sys.maxsize
        for child in nextStates:
            new_state = minimax(child,True, startTime, alpha, beta, depth+1)
            bestVal = min(bestVal, get_static_score(new_state))
            beta = min(beta, bestVal)
            if beta <= alpha: #Found a solution
                break
        return child

##########################################################################
# SCORING RELATED LOGIC

STATIC_SCORES={}

#def calculate_single_piece_static_evals():
#    for r in range(M):
#        for c in range(N):
#            for piece in range(3):
#                h = Z_NUM[r][c]
#                piece = PIECE_VAL(INITIAL_BOARD[r][c])  # piece at board[r][c]
#                h = h ^ Z_NUM[r * M + c][piece]

def diagonals(mat):
    global M, N
    def diag(sx, sy):
        for x, y in zip(range(sx, M), range(sy, N)):
            yield mat[x][y]
    for sx in range(M):
        yield list(diag(sx, 0))
    for sy in range(1, N):
        yield list(diag(0, sy))

def get_static_score(state):
    'Calls static eval function for newly seen board, else returns precomputed value'
    global Z_SCORES
    zcode = zhash(state[0])
    if zcode in Z_SCORES: #pre-computed value
        return Z_SCORES[zcode]

    else: #new board config
        score = staticEval(state)
        Z_SCORES[zcode] = score
        return score


def staticEval(state):
    global M, N
    board = state[0]
    whoseTurn = state[1]

    rows = []
    cols = []
    diags = list(diagonals(board))

    for j in range(N):
        cols.append([])

    #Find number of rows with K in a row
    for i in range(0,M):
        rows.append(board[i])
        for j in range(0,N):
            piece = board[i][j]
            cols[j].append(piece)


    all_lines = []

    if N>=K:
        flat_rows = flatten(rows)
        all_lines.extend(flat_rows)

    if M >=K:
        flat_cols = flatten(cols)
        all_lines.extend(flat_cols)

    flat_diags = flatten(diags)
    flat_diags = [d for d in flat_diags if len(d) >=K]

    all_lines.extend(flat_diags)


    score = 0
    threats =  0

    # more than 1, 2,.. K-1 in line
    for line in all_lines:
        l = len(line)
        mine =  line.count(MY_SIDE)
        yours = line.count(OPP_SIDE)
        forbidden = line.count('_')
        open = line.count('.')

#        threats =
        for k in range(1, K):
            #number in a line
            #continuous occurrences in a line, needs more than 2

            if k > 1:
                score += 10^k * line.count(MY_SIDE*k)
                score -= 10^k * line.count(OPP_SIDE*k)

        score = score + (5*mine) - (5*yours)

    #ensure if threat exists, it is noticed
    if OPP_SIDE == whoseTurn:
        score -= 10^k

    #threat_level = K-curr
    return score


def flatten(lines):
    'Reduce a list of lines to single strings for each row/column/diagonal'
    flat_lines = []
    for line in lines:
        new_line = ''.join(piece if piece!=' ' else '.' for piece in line)
        flat_lines.append(new_line)
    return flat_lines


# FACTORS to consider
# number of 1,2,... K-1 in line
# continuous 1,2,... K-1 in line
# threats !
# length of line itself
# Needed K  for win
# Number of available spots in row
# number of overall available spots
# Whoever is playing gets a basic advantage for same board orientation


##########################################################################
# CONVERSATIONAL LOGIC

"""
lose, win, game, play, player, loser, winner, tough, easy, puzzle, move, go, stop, start, finish, close
saved game, blocked you
"""

def respond(currentState, currentRemark):
    score = get_static_score(currentState[0])



    return "Aha"
##########################################################################
# Add zhash
# Find threats and stop them