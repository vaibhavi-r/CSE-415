'''luos9KInARow.py
Shiyi Luo, CSE 415, Autumn 2017, University of Washington
Instructor:  S. Tanimoto.
Assignment 5 : Game-Playing Agents
'''
from random import randint, choice
import copy
import time
import re

#initialize needed properties
h = 0
w = 0 
value_k = 0
side_I_play= "" 
opponent_name = ""
forbid_position = []
whole_list = [] #diagonal lines lists

def prepare(initial_state, k, what_side_I_play,opponent_nickname):
    #allow agent to get needed properties of the game board
    global h,w,value_k,forbid_position,side_I_play,opponent_name,whole_list
    h = len(initial_state[0])    # height of board
    w = len(initial_state[0][0]) # width of board
    value_k = k
    side_I_play = what_side_I_play
    opponent_name = opponent_nickname
    whole_list = getDiagonalList(w,h)
    for i in range(h):
        for j in range(w):
            if initial_state[0][i][j] == '-':
                forbid_position.append((i,j)) #cordinate the forbidden squares
    return "OK"
      
def introduce():
    return '''I am Tark Shadder, Shiyi Luo(luos9) created me. 
              I am a very friendly "K In A Row" game player.'''

def nickname():
    return "Tark"

def staticEval(state):
    #return the static evaluation value for "side_I_play"
    staticEValue = 0
    for num in range(2,value_k+1):
        xInARow = countKInARow(state[0],"X",num)
        oInARow = countKInARow(state[0],"O",num)
        if num == value_k and xInARow > 0: #'X' wins with high score
            staticEValue = pow(10,num+3)
        elif num == value_k and oInARow > 0: #'O' wins with low score
            staticEValue = -pow(10,num+3)
        else:
            staticEValue += pow(10,num)*xInARow - pow(10,num)*oInARow
    return staticEValue


def minmax(state, timeLimit, startTime, roundLeft):
    global side_I_play
    now = time.time()
    newState = []
    who = state[1]
    #if exceed accepatble running time or there's no round to play: return
    if now-startTime >= timeLimit*0.75 or roundLeft == 0:
        return [staticEval(state),state]
    if who == side_I_play:
        value = -1000000000 #large negative number
    else:
        value = 1000000000 #large postive number
    for i in possibleNextStates(state):
        newValue = minmax(i, timeLimit, startTime, roundLeft-1)[0]
        if (who == side_I_play and newValue > value) or (who == anti(side_I_play) and newValue < value):
            value = newValue
            newState = i
    return [value,newState] 

def makeMove(currentState, currentRemark, timeLimit=10000):
    startTime = time.time()
    result = minmax(currentState, timeLimit, startTime, 2)
    newState = result[1]
    value = result[0]
    move_x = 0
    move_y = 0
    newRemark = getRemark(currentState,currentRemark)
    for i in range(h):
        for j in range(w):
            if currentState[0][i][j] != newState[0][i][j]:
                move_x = i
                move_y = j #get the square of last move 
                break
    move = (move_x,move_y)
    return [[move,newState],newRemark]
     

def countKInARow(board,who,num):
    #return the number of num-in-a-row for "who" tokens
    h = len(board)
    w = len(board[0])
    score = 0
    
    #count vertical num-in-a-row score
    for i in range(w):
        lst = [j[i] for j in board]
        col = getIndex(who,lst)
        if len(col) == num:
            count = 0
            for i in range(num-1):
                if abs(col[i+1] - col[i]) == 1:
                    count += 1
            if count == num-1:
                score += 1  

          
    #count horizontal num-in-a-row score
    for i in range(h):
        lst = board[i]
        col = getIndex(who,lst)
        if len(col) == num:
            count = 0
            for i in range(num-1):
                if abs(col[i+1] - col[i]) == 1:
                    count += 1
            if count == num-1:
                score += 1  
    
    #count diagonal num-in-a-row score

    for i in whole_list:
        lst = []
        for j in i:
            lst.append(board[j[0]][j[1]])
        col = getIndex(who,lst)
        if len(col) == num:
            count = 0
            for i in range(num-1):
                if abs(col[i+1] - col[i]) == 1:
                    count += 1
            if count == num-1:
                score += 1  
    #return the total number of num-in-a-raw tokens on the board
    
    return score

#help funtions:
def getIndex(who,lst):
    occurrences = lambda s, lst: (i for i,e in enumerate(lst) if e == s)
    return list(occurrences(who, lst))

#get all possible next states for current states
def possibleNextStates(s):
    global h,w
    board = s[0]
    who = s[1]
    nextStates = []
    for i in range(h):
        for j in range(w):
            if board[i][j] == ' ':
               boardCopy = copy.deepcopy(board)
               boardCopy[i][j] = who #place the token at current square
               newState = [boardCopy,anti(who)]
               nextStates.append(newState)
    return nextStates

#whose term next
def anti(who): 
    if who == 'X':
        return 'O'
    elif who == 'O':
        return 'X'
    else:
        raise Exception('Illegal input')

#help funtion to return all diagonal lines

def getDiagonalList(w,h):
    for i in range(1,h+w-2):
        diagonal_list = []
        for j in range(h):
            for k in range(w):
                if j+k == i and (j,k) not in forbid_position:
                    diagonal_list.append((j,k))
        whole_list.append(diagonal_list)
    
    for i in range(h):
        diagonal_list = []
        j = 0
        if (i,j) not in forbid_position:
            diagonal_list.append((i,j))
        while i < h-1:
            i += 1
            j += 1
            if (i,j) not in forbid_position:
                diagonal_list.append((i,j))
        if diagonal_list !=[]:
            whole_list.append(diagonal_list)
            
    for i in range(w):
        diagonal_list_re = []
        j = 0
        if (j,i) not in forbid_position:
            diagonal_list_re.append((j,i))
        while i < w-1:
            i += 1
            j += 1
            if (j,i) not in forbid_position:
                diagonal_list_re.append((j,i))                
        if diagonal_list_re !=[] and diagonal_list_re not in whole_list:
            whole_list.append(diagonal_list_re)
    
        return [i for i in whole_list if len(i)>1]

def getRemark(currentState,currentRemark):
    global value_k
    score = staticEval(currentState)
    wrdlst = re.sub("[^\w]", " ",  currentRemark).split()
    wrdlst = [i.lower() for i in wrdlst]
    
    winRemark=["Haha I win, but you are so close!","Don't give up my friend, you wanna try again?"]
    loseRemark = ["Good game! you defeated me, I need go and practice more.","Congrats! You won, but I won't give up!","You are really good at playing this game, hey winner you wanna another round?"]
    advRemark = ["Hey come on, you can do it!","Watch out! I am leading now..","Be careful my friend, take your time before move!"]
    disadvRemark =["You did so well, give me some time.","Oh..it's getting harder for me,let me see", "Oops, I need to catch up","Clever move! I should be careful.."]
    tieRemark = ["It's a tie here! Come on, show me what you got.","Now we on the same spot, go ahead!"]
    friendlyRemark = ["Go ahead!","Nice move!","Humm,it's getting more and more interesting","Clever you! I need some time","I can tell you practice this a lot, ineresting!"]

    #showing awareness of the game state and game dynamics with personality            
    if score == pow(10,value_k+3):
        newRemark = choice(winRemark)
    elif score == -pow(10,value_k+3):
        newRemark = choice(loseRemark)
    elif score == 0:
        newRemark = choice(tieRemark)
    elif score > pow(10,value_k-1):
        newRemark = choice(advRemark)
    elif score < - pow(10,value_k-1):
        newRemark = choice(disadvRemark)
    else:
        #responding to the opponent's remarks
        for i in wrdlst:
            for j in ["win","ahead","lead","advan"]:
                if "i" in wrdlst and j in i:
                    return  "You are leading the game, I will catch up you!"
                else:
                    #present character for my agent
                    newRemark = choice(friendlyRemark)
    return newRemark
