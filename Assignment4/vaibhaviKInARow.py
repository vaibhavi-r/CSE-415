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

# Z SCORE RELATED
PIECE_VAL = {'O':1, 'X':2} #, '-':3 , ' ':4}
Z_NUM =[]  #2d array of size (MxN) by 2 (positions x pieces)
Z_SCORES ={} #Static State Evals stored without iteration depth


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

    #print("PREPARING")
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

    init_zobrist()
    parse_initial_board()

    return "OK"

def parse_initial_board():
    global NUM_O, NUM_X, NUM_FORBIDDEN_SPOTS, NUM_FILLED_SPOTS
    global OPEN_SPOTS, NUM_AVAILABLE_SPOTS

    #print("parse initial board")
    for i in range(M):
        for j in range(N):
            tile = INITIAL_BOARD[i][j]
            if tile == ' ':
                OPEN_SPOTS.append([i,j])
            elif tile == 'X':
                NUM_X +=1
                NUM_FILLED_SPOTS +=1
            elif tile == 'O':
                NUM_O += 1
                NUM_FILLED_SPOTS +=1
            else:
                NUM_FORBIDDEN_SPOTS += 1

    NUM_AVAILABLE_SPOTS = len(OPEN_SPOTS)
    #print("OPEN SPOTS initialized", OPEN_SPOTS)


############################################################
# ZOBRIST HASHING
def init_zobrist():
    #print("init zobrist")
    global Z_NUM
    global Z_SCORES

    Z_SCORES = {}

    # fill Z table with random numbers/bitstrings
    #print("Initializing Zobrist Table for Board Size:",M,'by',N)
    for tile in range(M*N):  # loop over the board as a linear array
        Z_NUM.append([[],[],[]])
        for piece in range(3):  # loop over the pieces
            Z_NUM[tile][piece] = random.getrandbits(32)
    #print("Z_NUM table", len(Z_NUM), len(Z_NUM[0]), Z_NUM)

def zhash(board):
    global Z_NUM, M, N
    h=0
    #print('zhash--')
    #print("BOARD", board)
    for r in range(M):
        for c in range(N):
            if board[r][c] != ' ' and board[r][c] != '-':
                #print("Found piece:", board[r][c])
                piece = PIECE_VAL[board[r][c]] #piece at board[r][c]
                h = h^Z_NUM[r*M+c][piece]
    #print("END zhash")
    return str(h)

############################################################
# MOVE MAKING LOGIC

def makeMove(currentState, currentRemark, timeLimit=10000):
    #print("makeMove")
    global TIME_LIMIT

    now = time.time()
    TIME_LIMIT = timeLimit

    currentBoard  = currentState[0]
    whoseTurn = currentState[1]

    if whoseTurn!=MY_SIDE:
        print("What's happening!")

    #find only open spots to generate successors
    update_open_spots(currentBoard)

    init_alpha = -sys.maxsize
    init_beta  = sys.maxsize
    init_depth = K/2

    newState = minimax(currentState, isMaxPlayer=True, startTime=now, alpha=init_alpha, beta=init_beta, depth=init_depth)

    move = getMove(currentState, newState)
    #print("OPEN SPOTS before:", OPEN_SPOTS)
    #print("MOVE", move)

    if move==None:
        print("Unable to find possible Move!")

    newRemark = respond(currentState,currentRemark)
    return [[move, newState], newRemark]

    #print("END makeMove")

def update_open_spots(board):
    global  OPEN_SPOTS, NUM_AVAILABLE_SPOTS
    OPEN_SPOTS= []
    for i in range(M):
        for j in range(N):
            if board[i][j]==' ':
                OPEN_SPOTS.append([i,j])
    NUM_AVAILABLE_SPOTS = len(OPEN_SPOTS)

def getMove(state, newState):
    #print("getMove")
    board = state[0]
    newBoard = newState[0]

    #print("OLD BOARD - ",board)
   # print("NEW BOARD - ",newBoard)

    #expect only one row will change
    for spot in OPEN_SPOTS:
        i = spot[0]
        j = spot[1]
        if board[i][j] != newBoard[i][j]:
            #print("END getMove - found it")
            return [i,j]
    #print("END getMove - none")
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
    #print("minimax")
    if depth<=0: #Time ran out
        #print("END minimax (0 Depth)")
        #print("No more depth")
        return state

    if TIME_LIMIT - (time.time() - startTime) <  0.2:
        #print("Timeout")
        #print("END minimax (TIMEOUT)")
        return state

    nextStates= successors(state)
    if nextStates ==[]:
        #print("END minimax (LEAF)")
        return state

    if isMaxPlayer == True:
        bestVal =  -sys.maxsize
        for child in nextStates:
            new_state = minimax(child, False, startTime, alpha, beta,  depth+1)
            bestVal = max(bestVal, get_static_score(new_state))
            alpha = max(alpha, bestVal)
            if beta <= alpha: #Found a solution
                break
        #print("END minimax (MAX)")
        return child

    else:
        bestVal = -sys.maxsize
        for child in nextStates:
            new_state = minimax(child,True, startTime, alpha, beta, depth+1)
            bestVal = min(bestVal, get_static_score(new_state))
            beta = min(beta, bestVal)
            if beta <= alpha: #Found a solution
                break
        #print("END minimax (MIN)")
        return child

def successors(state):
    #print("successors")
    'possible next states achievable from current state'
    board = state[0]
    currentPlayer = state[1]
    successorList = []

    #print("OPEN SPOTS (successors)", OPEN_SPOTS)

    for spot in OPEN_SPOTS:
        [i, j] = spot
        if board[i][j] == ' ':
            nextBoard = deepcopy(board)
            nextBoard[i][j] = currentPlayer
            nextPlayer = other(currentPlayer)
            successorList.append([nextBoard, nextPlayer])

        # Possibly order by static val?
        #print("Successors = ", len(successorList))
    #print("END successors")
    return successorList

##########################################################################
# SCORING RELATED LOGIC

#def calculate_single_piece_static_evals():
#    for r in range(M):
#        for c in range(N):
#            for piece in range(3):
#                h = Z_NUM[r][c]
#                piece = PIECE_VAL(INITIAL_BOARD[r][c])  # piece at board[r][c]
#                h = h ^ Z_NUM[r * M + c][piece]

def diagonals(mat):
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
        #print('known zcode')
        return Z_SCORES[zcode]

    else: #new board config
        #print('unknown zcode')
        score = staticEval(state)
        Z_SCORES[zcode] = score
        #print("END get static score")
        return score


def staticEval(state):
    #print('static eval')
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
    #print('END static eval')
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
    #print("respond")
    score = get_static_score(currentState)
#    if score > 0:
#        return "I might win"

    #print("END respond")
    return "Aha"
##########################################################################
# Add zhash
# Find threats and stop them