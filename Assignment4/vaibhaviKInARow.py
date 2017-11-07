# GLOBAL VARIABLES
INITIAL_STATE = []
INITIAL_PLAYER =
K =


############################################################
# INTRODUCTION
def introduce():
    intro = 'In an old house in Paris that was covered in vines \n'+\
            'lived twelve little girls in two straight lines.' +\
            'And I am a one of them, they call me, Madeline' +\
            'Vaibhavi (vaibhavi@uw.edu) is a teacher of mine' +\
            'I learnt K-In-A-Row from her by River Seine' +\
            'Now let us play, thanks to artificial design!'
    return intro

def nickname():
    'Who is this child genius who plays K In A Row?'
    return 'Madeline'

############################################################
# PREPARE
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    #ZobristHashing
    #

    return "OK"

#def zobrist_hashing():
#    return 1

############################################################
# MOVE MAKING LOGIC
def makeMove(currentState, currentRemark, timeLimit=10000):
    move = 0
    newState = currentState
    newRemark = utter()
    return [[move, newState], newRemark]

############################################################
# MINIMAX
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


#Iterative Deepening

##########################################################################
# STATE RELATED LOGIC

def staticEval(state):


    return 0

##########################################################################
# CONVERSATIONAL LOGIC
def utter():
    return "Aha"

"""
lose, win, game, play, player, loser, winner, tough, easy, puzzle, move, go, stop
"""

def respond(currentState, currentRemark):
    return "Aha"

##########################################################################