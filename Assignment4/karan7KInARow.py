import time, copy, math, random
from _sqlite3 import Row
from re import *

# GLOBAL VARIABLES
forbidden_squares = []
opponent_nick_name = ''
k_to_win = 0
my_side = ''
row_count = 0
column_count = 0 
moves_till_now = 0
total_possible_moves = 0
winning_diagonal_indices = []
best_move = []

def introduce():
    message = '''Hi I am AceBot. 
    I train everyday to become a champion (Tic-Tac-Toe / K In a Row) player.
    My creator is Karan Murthy (UWNetID: karan7)'''
    return message
    
def nickname():
    return 'AceBot'

def computeLeadingDiagonals(row, column, diagonal_indices):
    if row >= row_count or column >= column_count:
        return diagonal_indices
    if row < 0 or column < 0:
        return diagonal_indices
    if (row, column) not in diagonal_indices:    
        diagonal_indices.append((row, column))
    return computeLeadingDiagonals(row + 1, column + 1, diagonal_indices)

def computeAntiDiagonals(row, column, diagonal_indices):
    if row >= row_count or column >= column_count:
        return diagonal_indices
    if row < 0 or column < 0:
        return diagonal_indices
    if (row, column) not in diagonal_indices:
        diagonal_indices.append((row, column))
    return computeAntiDiagonals(row - 1, column + 1, diagonal_indices)

def prepare(initial_state, k, what_side_I_play, opponent_nickname):
    global forbidden_squares, opponent_nick_name, k_to_win, my_side, row_count, column_count, moves_till_now, total_possible_moves
    global winning_diagonal_indices
    k_to_win = k
    my_side = what_side_I_play
    opponent_nick_name = opponent_nickname
    board = initial_state[0]
    row_count = len(board)
    column_count = len(board[0])
    diagonal_indices = []
    
    for row in range(row_count):
        for col in range(column_count):
            if board[row][col] != '-':
                if board[row][col] != ' ':
                    moves_till_now += 1
                # Total possible moves indicates the total number of
                # moves possible till it's a draw or a win for
                # either player.
                total_possible_moves += 1
            else:
                forbidden_squares.append((row, col))
                
    # Computing leading and anti-diagonals
    min_row_col = min(row_count - 1, column_count - 1)
    row = min_row_col
    while(row >= 0):
        computeLeadingDiagonals(row, 0, diagonal_indices)
        if len(diagonal_indices) >= k_to_win and diagonal_indices not in winning_diagonal_indices:
            winning_diagonal_indices.append(diagonal_indices)
        diagonal_indices = []
        
        computeAntiDiagonals(row, 0, diagonal_indices)
        if len(diagonal_indices) >= k_to_win and diagonal_indices not in winning_diagonal_indices:
            winning_diagonal_indices.append(diagonal_indices)
        diagonal_indices = []
        row -= 1
        
    column = min_row_col
    while(column >= 0):
        computeLeadingDiagonals(0, column, diagonal_indices)
        if len(diagonal_indices) >= k_to_win and diagonal_indices not in winning_diagonal_indices:
            winning_diagonal_indices.append(diagonal_indices)
        diagonal_indices = []
        
        computeAntiDiagonals(0, column, diagonal_indices)
        if len(diagonal_indices) >= k_to_win and diagonal_indices not in winning_diagonal_indices:
            winning_diagonal_indices.append(diagonal_indices)
        diagonal_indices = []
        
        computeAntiDiagonals(min_row_col, column, diagonal_indices)
        if len(diagonal_indices) >= k_to_win and diagonal_indices not in winning_diagonal_indices:
            winning_diagonal_indices.append(diagonal_indices)
        diagonal_indices = []
        column -= 1 
            
    return 'OK'


def generateSuccessors(state, next_move):
    board = state[0]
    successors = []
    try:
        for row in range(row_count):
            for col in range(column_count):
                if board[row][col] == ' ':
                    temp_board = copy.deepcopy(board)
                    temp_board[row][col] = next_move
                    new_state = [temp_board, retrieveOpponent(next_move)]
                    successors.append(new_state)
    except Exception as e:
        print ('Error occured in generateSuccessors') 
        raise
    return successors

def minimax(current_state, depth_limit, start_time, timeLimit, alpha = float('-inf'), beta = float('inf')):
    next_state = []
    global best_move
    try:
        if time.time() - start_time >= (0.9 * timeLimit):
            return [current_state, staticEval(current_state)]
        if depth_limit == 0:
            return [current_state, staticEval(current_state)]
        next_move = current_state[1]
        if next_move == my_side:
            for state in generateSuccessors(current_state, next_move):
                result = minimax(state, depth_limit - 1, start_time, timeLimit)
                new_score = result[1]
                if new_score > alpha:
                    alpha = new_score
                    next_state = state
                    best_move = [next_state, alpha]
                    
                if beta <= alpha:
                    break
            return best_move
        else:
            for state in generateSuccessors(current_state, next_move):
                result = minimax(state, depth_limit - 1, start_time, timeLimit)
                new_score = result[1]
                if new_score < beta:
                    beta = new_score
                    next_state = state
                    best_move = [next_state, beta]
                
                if beta <= alpha:
                    break
            return best_move
        
    except Exception as e:
        print ('Error occured in minimax') 
        raise
   
def makeMove(currentState, currentRemark, timeLimit=5):
    start_time = time.time()
    depth_limit = 2
    values_returned = minimax(currentState, depth_limit, start_time, timeLimit, float('-inf'), float('inf'))
    if values_returned == None:
        values_returned = best_move
    new_state = values_returned[0]
    eval_score = values_returned[1]
    updated_row = 0
    updated_col = 0
    global moves_till_now
    changeFound = False
    for row in range(row_count):
        for col in range(column_count):
            if new_state[0][row][col] != currentState[0][row][col]:
                    updated_row = row
                    updated_col = col
                    changeFound = True
                    break
        if changeFound:
            break
    

    moves_till_now += 2          
    new_remark = respond(currentRemark)
    return [[(updated_row, updated_col), new_state], new_remark]


def retrieveOpponent(side):
    if side == 'X': return 'O'
    elif side == 'O': return 'X'
    else: return null

def retrieveScore(my_count, opponent_count, num):
    # Increment the eval score to keep things moving    
    return (my_count - opponent_count) * pow(10, num)

def analyzeBoard(board, num):
    eval_score = 0
    flag = False
    my_count = 0
    opponent_count = 0
    opponent = retrieveOpponent(my_side)
    count_difference = 0
    
    try:
    # HORIZONTAL COMPUTATION
        for row in range(row_count):
            for col in range(column_count):
                if board[row][col] == opponent:
                    opponent_count += 1
                elif board[row][col] == my_side:
                    my_count += 1   
            
            eval_score += retrieveScore(my_count, opponent_count, num)
            my_count = 0
            opponent_count = 0

    
        # VERTICAL COMPUTATION
        for col in range(column_count):
            for row in range(row_count):    
                if board[row][col] == opponent:
                    opponent_count += 1
                elif board[row][col] == my_side:
                    my_count += 1    
            eval_score += retrieveScore(my_count, opponent_count, num)  
            my_count = 0
            opponent_count = 0
                
        #DIAGONAL WINNING COMBINATIONS
        for diagonal_indices in winning_diagonal_indices:
            for row, col in diagonal_indices:
                if board[row][col] == opponent:
                    opponent_count += 1
                elif board[row][col] == my_side:
                    my_count += 1    
            eval_score += retrieveScore(my_count, opponent_count, num)
            my_count = 0
            opponent_count = 0             
                       
    except Exception as e:
        print ('Error occured in retrieveScore') 
        raise    
         
    return eval_score          

def staticEval(state):
    static_eval_score = 0
    whosePlaying = state[1]
    for num in range(1, k_to_win + 1):
        static_eval_score += analyzeBoard(state[0], num)
    return static_eval_score


# Code for the conversational part
CASE_MAP = {'i':'you', 'I':'you', 'me':'you', 'you':'me',
            'my':'your', 'your':'my',
            'yours':'mine', 'mine':'yours', 'am':'are'}

punctuation_pattern = compile(r'\,|\.|\?|\!|\;|\:|\"')  

def you_me(w):
    'Changes a word from 1st to 2nd person or vice-versa.'
    try:
        result = CASE_MAP[w]
    except KeyError:
        result = w
    return result

def you_me_map(wordlist):
    'Applies YOU-ME to a whole sentence or phrase.'
    return [you_me(w) for w in wordlist]

def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern, '', text)    

def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when', 'why', 'where', 'how', 'what'])

def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)

def respond(currentRemark):
    initial_remarks = ['Common make a move, who are you waiting for?', 'It is gonna be fun placing those Xs and Os', 
                       'I am ' + my_side + ' and you are ' + retrieveOpponent(my_side)]
    midway_remarks = ['How is that move?', 'Like that move?', 'Take that', 'Yeah I am getting better',
                      "Did't I ace that move", 'The word give up does not exist in my dictionary']
    last_stage_remarks = ['I am going to win this', 'That is why they call me AceBot', 
                          "It is gonna be easy cause you don't know any better"]
    
    wordlist = split(' ', remove_punctuation(currentRemark).strip())
    # Remove any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)

    if 'good' in wordlist:
        return "No you're not good. " + currentRemark

    if 'better' in wordlist:
        return "No you're not better " + stringify(mapped_wordlist[mapped_wordlist.index('better') + 1:]) \
            + ". " + currentRemark
    
    if 'best' in wordlist:
        return "No you're not the best. " + currentRemark
    
    if 'beat' in wordlist:
        return "No you cannot beat " + stringify(mapped_wordlist[mapped_wordlist.index('beat') + 1:]) \
            + ". " + currentRemark
            
    if 'win' in wordlist:
        return "No you cannot win " + stringify(mapped_wordlist[mapped_wordlist.index('win') + 1:]) \
            + ". " + currentRemark           
    
    if wpred(wordlist[0]):
        return "You tell me " + stringify(mapped_wordlist) + "."
    
    if moves_till_now <= (1/3 * total_possible_moves):
        return random.choice(initial_remarks)
    elif moves_till_now >= (2/3 * total_possible_moves):
        return random.choice(last_stage_remarks)
    
    return random.choice(midway_remarks) 
