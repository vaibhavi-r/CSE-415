'''
vaibhaviKInARow.py
Author: Vaibhavi Rangarajan
OPTION B: K-in-a-Row with Forbidden Squares.
'''
from random import getrandbits
from random import choice
import time
from copy import deepcopy
import sys
import collections

#STATE VARIABLES
global NEW_STATE


# START VARIABLES
INITIAL_PLAYER = ''
INITIAL_BOARD = []


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
    global OPEN_SPOTS, NUM_AVAILABLE_SPOTS, NUM_FORBIDDEN_SPOTS

    #print("parse initial board")
    for i in range(M):
        for j in range(N):
            tile = INITIAL_BOARD[i][j]
            if tile == ' ':
                OPEN_SPOTS.append([i,j])
            elif tile == '-':
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
            Z_NUM[tile][piece] = getrandbits(32)
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

    newRemark = respond(currentState, newState, move, currentRemark)
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

    if TIME_LIMIT - (time.time() - startTime) <  0.25:
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


    #reduce to minimal number of unique line patters
    unique_lines = collections.Counter(all_lines)

    score = 0

    # more than 1, 2,.. K-1 in line
    for line in unique_lines:
        l = len(line)
        freq = unique_lines[line]

        ######Score based on threats, and bad positions : K-1, K-2 in a row  (MAJOR IMPACT)
        dot = '.'
        block = '-'
        bad_pattern_my = MY_SIDE*(K-2)
        bad_pattern_you = OPP_SIDE*(K-2)
        threat_pattern_my = MY_SIDE*(K-1)
        threat_pattern_you = OPP_SIDE *(K-1)

        #BAD/GOOD = K-2 elements open on 1 or 2 sides
        bad1_my = line.count(dot+bad_pattern_my + block)    + line.count(block+bad_pattern_my+dot)+\
                  line.count(dot+bad_pattern_my + OPP_SIDE) + line.count(OPP_SIDE+bad_pattern_my+dot)
        bad1_you = line.count(dot + bad_pattern_you + block) + line.count(block + bad_pattern_you + dot) + \
                  line.count(dot + bad_pattern_you + MY_SIDE) + line.count(MY_SIDE + bad_pattern_you + dot)

        bad2_my = line.count(dot+bad_pattern_my+dot)
        bad2_you = line.count(dot+bad_pattern_you+dot)


        #THREAT = K-1 elements open on 1 or 2 sides
        threat1_my = line.count(dot + threat_pattern_my + block) + line.count(block + threat_pattern_my + dot) + \
                  line.count(dot + threat_pattern_my + OPP_SIDE) + line.count(OPP_SIDE + threat_pattern_my + dot)
        threat1_you = line.count(dot + threat_pattern_you + block) + line.count(block + threat_pattern_you + dot) + \
                   line.count(dot + threat_pattern_you + MY_SIDE) + line.count(MY_SIDE + threat_pattern_you + dot)

        threat2_my = line.count(dot + threat_pattern_my + dot)
        threat2_you = line.count(dot + threat_pattern_you + dot)

        score += 4^(bad1_my*freq) + 9^(bad1_my*freq) + 100^(threat1_my*freq) + 200^(threat2_my*freq)
        score -= 5^(bad1_you*freq) + 10^(bad1_you*freq) + 1000^(threat1_you*freq) + 2000^(threat2_you*freq)

        ###### Score based on how many in a line (MINOR IMPACT)
        for k in range(2, K-2):
            #number in a line
            #continuous occurrences in a line, needs more than 2
            mine_continuous = line.count(dot+(MY_SIDE*k) + dot)
            you_continuous = line.count(dot +(OPP_SIDE*k) + dot)
            score += (3^k)*mine_continuous*freq
            score -= (4^k)*you_continuous*freq

        #mine = line.count(MY_SIDE)  # how many
        #yours = line.count(OPP_SIDE)  # how many


    #ensure if threat/bad exists, it is noticed and actionable
    if MY_SIDE == whoseTurn:
        score += 1000

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

def respond(currentState, newState, move, currentRemark):
    """ Madeline derives from the adventurous, young, French cartoon namesake.
    Personality: Adventurous, and enthusiastic. Speaks in rhymes.
    """
    #print("respond")
    if NUM_AVAILABLE_SPOTS <=1:
        return "And then there were none. Looks like the game is done."

    if move == None:
        return "You are clever, mon ami. This game has flummoxed me."

    if choice([0,1])%2==0:
        #Respond to Opponent

        words = currentRemark.lower().split(" ")
        win_comment = "If I win this game today, you will have to do as I say."
        lose_comment = "Let us hope I dont lose. To speak with you, I will refuse."
        tough_comment = "Dont give up if this feels tough, lets get to the end, thats enough "
        stop_comment = "We should stop and place a bet? For the prize of a baguette."
        play_comment = "It is so much fun to play with you! Do you feel the same too?"
        easy_comment = "Isnt this game easy, I think "
        move_comment = "I want to move here and there, until no more spots are there"
        finish_comment = "It is getting close to the end. Will we still be friends?"
        good_comment = "This just went from good to great . We will be here till late"
        block_comment = "Sometimes you block another, sometimes you get blocked by mother"
        you_comment = "I dont like to talk about me, but I will, " + OPP_NAME + "you are like family"

        candidates = {"win": win_comment,
                      "lose": lose_comment,
                      "loser":lose_comment,
                      "winner":win_comment,
                      "player": play_comment,
                      "tough":easy_comment,
                      "easy":tough_comment,
                      "move":move_comment,
                      "stop":stop_comment,
                      "finish":finish_comment,
                      "good":good_comment,
                      "block" : block_comment,
                      "you": you_comment
                      }
        for trigger in candidates:
            if trigger in words:
                return candidates[trigger]
        return "Tomorrow at lunchtime we can meet and prep, would you care for some baguette and crepes?"

    else:
        #Respond to Game State
        forbid_comment = "We started with " + str(NUM_FORBIDDEN_SPOTS) +" forbidden spaces . And we've moved a few paces ."
        base_comment   = "I might need to go in a new direction . If only I were a kid mathematician ."
        init_comment = str(INITIAL_PLAYER) + " has a start advantage, you know . What are the chances of " + str(K) + " in a row ?"

        if move[0]==move[1]:
            diag_comment = "I like to run zigzag in the park, And on this diagonal, I place my mark"
        elif move[0]==0 or move[0]==M-1:
            diag_comment= "I am keeping close to the edge now. You can keep the rest "
        else:
            diag_comment= "At " + str(move[0]) + " and " + str(move[1]) + " this counter I place. Your move now, pick up the pace. "

        score = get_static_score(currentState)
        new_score = get_static_score(newState)
        diff = new_score - score
        if diff > 1000:
            diff_comment = "Yay! This might do the trick. A few more moves to win this quick."
        elif diff < 0:
            diff_comment = "Sacre Bleu, it cannot be! Am I worse off than I thought I'd be ?"
        else:
            diff_comment = "Not much has changed from in this move. If I win , I'll take you to the Loevre !"

        return choice([forbid_comment, init_comment, base_comment, diff_comment, diag_comment])

    return "Aha"

##########################################################################