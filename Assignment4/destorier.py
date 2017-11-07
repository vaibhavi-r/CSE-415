'''ldfghhKlnARow.py
CSE 415 Assignment5
May 9th 2017
Difei Lu
This program generates a agent which will be able to play a KInARow game with other agent
'''

from random import randint
from copy import deepcopy
import time


def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    '''record the initial state of the game.'''
    global my_state, self_side, oppo_side, oppo_name, mRows, nColumns, size

    size = k

    my_state = initial_state
    size = k
    self_side = what_side_I_play
    oppo_name = opponent_nickname

    if self_side == 'X':
        oppo_side = 'O'
    elif self_side == 'O':
        oppo_side = 'X'
    else:
        return "Error: what_side_I_play must be X or O"

    mRows = len(my_state[0])
    nColumns = len(my_state[0][0])

    return "OK"


def introduce():
    '''Introcuce my agent'''
    return "My pathetic opponent, I am the destorier, developed by Difei Lu.\
            Don't be sad if I beat you, because you are not the only one."


def nickname():
    '''Return a short version of the playing agent's name'''
    return "Destorier"


def makeMove(currentState, currentRemark, timeLimit=10000):
    '''make a move based on nimiMax search'''
    MIN = -100000
    MAX = 100000
    plyLeft = 3
    start = time.time()
    newState = miniMax(currentState, plyLeft, MIN, MAX, start, timeLimit)
    list = ["You know that it's over.", "You are dominated.", "Good move, you've earned my respect.",
            "You just committed suicide.", "That's truly a desperate move.",
            "You are too weak to fight against me.", "Poor man, you just lost."]
    ranNum = randint(0, 6)
    newRemark = list[ranNum]
    move = get_move(currentState, newState)
    return [[move, newState], newRemark]


def staticEval(b, side):
    '''For each segment with size k in rows, columns and diagonals,
       Add 10 ^ (number of side_mark - 1) to evaluation score.'''
    score = 0
    sum = get_row(b) + get_col(b) + get_diagonals(b, 0) + get_diagonals(b, 1)
    segments = []
    for lst in sum:
        if len(lst) >= size:
            for i in range(len(lst) - size + 1):
                segment = lst[i: i + size]
                segments.append(segment)
    for segment in segments:
        count = 0
        for cell in segment:
            if cell == side:
                count += 1
            elif cell != ' ':
                count = 0
                break
        if count > 0:
            score += 10 ** (count - 1)
    return score


# Hepler method
def miniMax(s, plyLeft, MIN, MAX, start, timeLimit):
    '''Use miniMax to search for plyLeft levels,
       return the state which has greatest chance to win.'''
    if time.time() - start > timeLimit * 0.8:
        return s
    lst = sucessors(s)
    if plyLeft == 0 or lst == []:
        return s
    side = s[1]

    if side == 'X':
        # When my agent is on X side
        dyMin = MIN
        result = s
        for i in range(len(lst)):
            newState = miniMax(lst[i], plyLeft - 1, dyMin, MAX, start, timeLimit)
            newEval = staticEval(newState[0], 'X') - staticEval(newState[0], 'O')
            if newEval > dyMin:
                dyMin = newEval
                result = lst[i]
        return result

    else:
        # When my agent is on O side
        dyMax = MAX
        result = s
        for i in range(len(lst)):
            newState = miniMax(lst[i], plyLeft - 1, MIN, dyMax, start, timeLimit)
            newEval = staticEval(newState[0], 'X') - staticEval(newState[0], 'O')
            if newEval < dyMax:
                dyMax = newEval
                result = lst[i]
        return result


def sucessors(s):
    b = s[0]
    side = s[1]
    result = []
    for i in range(mRows):
        for j in range(nColumns):
            if b[i][j] == ' ':
                sucessor = deepcopy(b)
                sucessor[i][j] = side
                result.append([sucessor, switch_side(side)])
    return result


def switch_side(side):
    if side == 'X': return 'O'
    elif side == 'O': return 'X'
    else: return ''


def get_move(s1, s2):
    ''' Return the move to new state'''
    b1 = s1[0]
    b2 = s2[0]
    for i in range(len(b1)):
        for j in range(len(b1[i])):
            if b1[i][j] != b2[i][j]:
                return [i, j]


def get_row(b):
    '''Return a list of rows.'''
    return [[cell for cell in row] for row in b]


def get_col(b):
    '''Return a list of columns.'''
    c = [[] for col in b[0]]
    for row in b:
        for i, cell in enumerate(row):
            c[i].append(cell)
    return c


def get_diagonals(b, direction):
    '''Return a list of diagonals.
    0 for backward(\), 1 for forward(/)'''
    buffer = ['A'] * (len(b[0]) + 1)
    grid = []
    for i, r in enumerate(get_row(b)):
        if direction == 0:
            grid.append(buffer[i:] + r + buffer[:i + 1])
        elif direction == 1:
            grid.append(buffer[:i + 1] + r + buffer[i:])
    if direction == 0:
        c = get_col(grid)[2:-1]
    elif direction == 1:
        c = get_col(grid)[1:-2]
    for col in c:
        while 'A' in col:
            col.remove('A')
    return c
