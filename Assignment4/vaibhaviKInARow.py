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
    #init_zobrist()
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

PIECE_VAL = {'O':1, 'X':2}#, '-':3 , ' ':4}
Z_NUM =[]  #2d array of size (MxN) by 4 (positions x pieces)
Z_SCORES ={} #State Evals stored with iteration depth

def init_zobrist():
    global M, N
    global Z_NUM
    # fill Z table with random numbers/bitstrings

    print("Initializing Zobrist Table for Board Size:",M,'by',N)
    for tile in range(M*N):  # loop over the board as a linear array
        Z_NUM.append([[],[],[],[]])
        for piece in range(2):  # loop over the pieces
            Z_NUM[tile][piece] = random.getrandbits(10)


def zhash(board):
    h=0
    for r in range(M):
        for c in range(N):
            if board[r][c] != ' ' and board[r][c] != '-':
                print("Found piece:", board[r][c])
                piece = PIECE_VAL[board[r][c]] #piece at board[r][c]
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
    print("Successors = ", len(successorList))
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
    init_depth = 1

    #newState = minimax(currentState, isMaxPlayer=True, startTime=now, alpha=init_alpha, beta=init_beta, depth=init_depth)
    [newVal, newState] = minimax2(currentState, TIME_LIMIT, now , init_depth)

    #print("Found New Board ", newState[0])

    move = getMove(currentState, newState)
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

        #changes = [(i, e1, e2) for i, (e1, e2) in enumerate(zip(list1, list2)) if e1 != e2]
        #NUM_AVAILABLE_SPOTS -=1
        #move_i = [i for i in list1 + list2 if (a not in list1) or (a not in list2)]

##########################################################################
# MINIMAX RELATED LOGIC

def other(current_player):
    if current_player =='X':
        return 'O'
    elif current_player == 'O':
        return 'X'
    else: print("Error in switching sides")


def minimax2(state, timeLimit, timeStart, playLeft):
    global MY_SIDE

    print(time.time()-timeStart)
    print("Time Limit", timeLimit)
    if time.time() - timeStart >= timeLimit * 0.7:
        return [staticEval(state), state]
    nextState = []
    whichSide = state[1]
    if (playLeft == 0): return [staticEval(state), state]
    if whichSide == MY_SIDE: provisional = -900000000
    else: provisional = 900000000
    for everyState in successors(state):
        everyResult = minimax2(everyState, timeLimit, timeStart, playLeft - 1)
        newVal = everyResult[0]
        if (whichSide == MY_SIDE and newVal > provisional) or (whichSide == other(MY_SIDE) and newVal < provisional):
            provisional = newVal
            nextState = everyState
    return [provisional, nextState]


'''
# MINIMAX with Alpha Beta Pruning
def minimax(state, isMaxPlayer, startTime, alpha, beta, depth=0):
    print("MINIMAX")

#    if depth<=0: #Time ran out
#        print("No more depth")
#        return state

    if (time.time() - startTime) >  0.8*TIME_LIMIT:
        print("Timeout")
        return state

    nextStates= successors(state)
    if nextStates ==[]:
        return state


    if isMaxPlayer == True:
        print("MAXPLAYER")
        bestVal =  -sys.maxsize
        for child in nextStates:
            new_state = minimax(child, False, startTime, alpha, beta,  depth+1)
            bestVal = max(bestVal, staticEval(new_state))
            alpha = max(alpha, bestVal)
            if beta <= alpha: #Found a solution
                break
        return child

    else:
        print("MINPLAYER")
        bestVal = -sys.maxsize
        for child in nextStates:
            new_state = minimax(child,True, startTime, alpha, beta, depth+1)
            bestVal = min(bestVal, staticEval(new_state))
            beta = min(beta, bestVal)
            if beta <= alpha: #Found a solution
                break
        return child
'''

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
    global M, N
    print("\tEVAL", M, N)

    board = state[0]
    whoseTurn = state[1]

    rows = []
    cols = []
    diags1 = []
    diags2 = []

    for j in range(N):
        cols.append([])

    #Find number of rows with K in a row
    for i in range(M):
        rows.append(board[i])
        for j in range(N):
            piece = board[i][j]
            cols[j].append(piece)
            #diags1[M-1+i].append(piece)

    all_lines = []

    flat_rows = flatten(rows)
    flat_cols = flatten(cols)
 #   flat_diags1 = flatten(diags1)
 #   flat_diags2 = flatten(diags2)

    all_lines.extend(flat_rows)
    all_lines.extend(flat_cols)
    print(all_lines)

 #   all_lines.extend(flat_diags1)
#    all_lines.extend(flat_diags2)

    print("\t SCORING")
    score = 0
    # more than 1, 2,.. K-1 in line
    for line in all_lines:
        for k in range(1, K):
            #number in a line
            score += 5^k * line.count('X')
            score -= 5^k * line.count('O')

            #continuous occurrences in a line, needs more than 2
            if k > 1:
                score += 10^k * line.count('X'*k)
                score -= 10^k * line.count('O'*k)

    #FACTORS to consider
    #number of 1,2,... K-1 in line
    #continuous 1,2,... K-1 in line
    #threats !
    #length of line itself
    # Needed K  for win
    # Number of available spots in row
    #number of overall available spots
    # Whoever is playing gets a basic advantage for same board orientation
    if MY_SIDE ==whoseTurn:
        score += 100

    return score

def flatten(lines):
    'Reduce a list of lines to single strings for each row/column/diagonal'
    flat_lines = []
    for line in lines:
        new_line = ''.join(piece for piece in line)
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