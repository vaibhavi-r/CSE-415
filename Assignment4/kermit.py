# Jiawei Zhang   1337686
# CSE 415 HW5   Option B
# K-In-A-Row

'''
jz34KInARow.py
A K-In-A-Row game agent
Win the game by having k consecutive same element in a line
(in a row, a column, or a diagonal)
'''


from random import randint
from copy import deepcopy
import time

height = 0
width = 0
kSize = 0
rows = []
columns = []
diagonals = []
isPlaying = ''
opponent = ''
zobristnum = []


def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    '''prepare the game before start'''
    global height
    global width
    global kSize
    global isPlaying
    global opponent
    global rows
    global columns
    global diagonals
    height = len(initial_state[0])
    width = len(initial_state[0][0])

    kSize = k
    isPlaying = what_side_I_play
    opponent = opponent_nickname
    #myinit()

    # find all the consecutive row, column, diagonal line that is equal or greater
    # than kSize without '-', record their coordinates
    board = initial_state[0]
    # record the kSize lines in rows
    for i in range(height):
        for j in range(width):
            if j + kSize <= width:
                jRow = []
                for j in range(j, j + kSize):
                    if board[i][j] == '-': break   # exclude '-' in board
                    jRow.append((i,j))
                if len(jRow) >= kSize:  # not contain '-'
                    rows.append(jRow)
    # record the kSize lines in columns
    for j in range(width):
        for i in range(height):
            if i + kSize <= height:
                iCol = []
                for i in range(i, i + kSize):
                    if board[i][j] == '-': break
                    iCol.append((i, j))
                if len(iCol) >= kSize:
                    columns.append(iCol)
    # record the kSize lines in diagonal in top-left to bottom-right direction
    for j in range(width):
        for i in range(height):
            if i + kSize <= height and j + kSize <= width:
                ijDiagonal1 = []
                temp = j
                for i in range(i , i + kSize):
                    if board[i][j] == '-': break
                    ijDiagonal1.append((i, temp))
                    temp += 1
                if len(ijDiagonal1) >= kSize:
                    diagonals.append(ijDiagonal1)
    # record the kSize lines in diagonal in bottom-left to top right direction
    for j in range(width):
        for i in range(height):
            if i - kSize >= -1 and j + kSize <= width:
                ijDiagonal2 = []
                temp = j
                for i in range(i, i - kSize, -1):
                    if board[i][j] == '-': break
                    ijDiagonal2.append((i, temp))
                    temp += 1
                if len(ijDiagonal2) >= kSize:
                    diagonals.append(ijDiagonal2)
    return 'OK'


def introduce():
    return  '''
            My name is Checkered Bandana, and I'm a K-In-A-Row game agent.
            I am irritable and rude. It's dangerous to play game with me.
            My creator is Jiawei Zhang (UWNetID: jz34).
            '''

def nickname():
    return 'Kermit'


def makeMove(currentState, currentRemark, timeLimit=1000):
    '''move deciding part'''
    startTime = time.time()
    [newVal, newState] = minimax(currentState, startTime, timeLimit, 1)
    newRemark = utterances(newVal, currentRemark)
    move = makeMoveHelper(currentState, newState)
    return [[move, newState], newRemark]


def minimax(state, startTime, timeLimit, plyLeft):
    '''minimax algorithm'''
    if timeLimit - (time.time() - startTime) < 0.1:
        return [staticEval(state), state]
    board = state[0]
    whoseMove = state[1]
    newState = state
    if plyLeft == 0:
        return [staticEval(state), state]
    if whoseMove == 'X':
        provisional = -100000
    else:
        provisional = 100000

    successorList = successors(state)
    for i in range(len(successorList)):
        [newVal, newState] = minimax(successorList[i], startTime, timeLimit, plyLeft - 1)
        if (whoseMove == 'X' and newVal > provisional) or \
                (whoseMove == 'O' and newVal < provisional):
            provisional = newVal
    return [staticEval(newState), newState]


def successors(state):
    '''all successors of current state'''
    board = state[0]
    whoseMove = state[1]
    successorList = []
    for i in range(height):
        for j in range(width):
            if board[i][j] == ' ':
                succboard = deepcopy(board)
                succboard[i][j] = whoseMove
                if whoseMove == 'X':
                    nextmove = 'O'
                else:
                    nextmove = 'X'
                successorList.append([succboard, nextmove])
    return successorList


def utterances(newVal, currentRemark):
    '''make a comment on each move based on the current score and opponent's remark'''
    newRemark = ''
    if 'beat you' or 'win you' or 'you lose' or 'you will lose' in currentRemark:
        newRemark += 'shut up, '
    if newVal >= 3000:
        newRemark += 'noob, I got this game!'
    if 3000 > newVal >= 2000:
        newRemark += 'easy game!'
    if 2000 > newVal >= 1000:
        newRemark += 'I am in advantage of this game!'
    if 1000 > newVal >= 0:
        newRemark += 'time to show you true power of me!'
    if 0 > newVal >= -1000:
        newRemark += 'looks like you have some good moves, but I still got this!'
    if -1000 > newVal >= -2000:
        newRemark += 'I will catch up!'
    if -2000 > newVal >= -3000:
        newRemark += 'damn!'
    if newVal <= -3000:
        newRemark += 'I will never lose this!'
    return opponent + ', ' + newRemark


def makeMoveHelper(currentState, newState):
    for i in range(len(currentState[0])):
        for j in range(len(newState[0])):
            if currentState[0][i][j] != newState[0][i][j]:
                return (i,j)

def staticEval(state):
    '''calculate the advantage of X and disadvantage of O'''
    global rows, columns, diagonals
    return staticEvalHelper(state, rows, columns, diagonals)


def staticEvalHelper(state, rows, columns, diagonals):
    '''helper func to calculate static evaluation'''
    Xcount = 0
    Ocount = 0
    board = state[0]
    for comboList in rows:
        for (i,j) in comboList:
            if board[i][j] == 'X':
                Xcount += 1
            if board[i][j] == 'O':
                Ocount += 1
    rowScore = getScore(Xcount, Ocount)
    Xcount = 0
    Ocount = 0
    for comboList in columns:
        for (i, j) in comboList:
            if board[i][j] == 'X':
                Xcount += 1
            if board[i][j] == 'O':
                Ocount += 1
    colScore = getScore(Xcount, Ocount)
    Xcount = 0
    Ocount = 0
    for comboList in diagonals:
        for (i, j) in comboList:
            if board[i][j] == 'X':
                Xcount += 1
            if board[i][j] == 'O':
                Ocount += 1
    diaScore = getScore(Xcount, Ocount)
    return rowScore + colScore + diaScore


def getScore(Xcount, Ocount):
    '''score calculator baseon on current nums of X and O'''
    global kSize
    score = 0
    if Xcount >= kSize:
        score += 1000
    if Xcount >= 2*Ocount:
        score += 300
    if Xcount > Ocount:
        score += 100
    if Ocount >= kSize:
        score -= 1000
    if Ocount >= 2*Xcount:
        score -= 300
    if Ocount > Xcount:
        score -= 100
    return score



'''for debug
state = \
              [[[' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ','X',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ','-',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' '],
                [' ',' ',' ',' ',' ',' ',' ']], "X"]
#print(state[0][1][1] == 'X')
print(prepare(state, 5, 'X', 'f'))
print(makeMove(state, 'win you', 1))
#print(staticEval(state))
#print(len(diagonals))
#print(minimax(state, 1, 10, 3))
'''