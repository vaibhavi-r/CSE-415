# Program inports
import random
import time
import copy

# Method 1: Here is my nickname
def nickname():
  return "Ships"
  
# Method 2: Greetings to the other player and the game master. Introducing myself
def introduce():
  return "I am Shipra. I like mind games and my favorite is Tic-Tac-Toe."

# Method 3: Tell me about the board details and my opponent. I'll get ready for the game
def prepare(initial_state, k, what_side_I_play, opponent_nickname):
  global K, myChar, numOfRows, numOfCols, targetWinOptions
  
  # Number of K (in a row) needed to win the game
  K = k
  myChar = what_side_I_play
  numOfRows = len(initial_state[0])
  numOfCols = len(initial_state[0][0])
  if K < 2 or K>numOfCols or K >numOfRows:
    print("Invalid K.")
    return
    
  # Calculating potential win options from the initial_state of the board
  targetWinOptions = [] # has the form [[(0,0),(0,1),(0,2),...], [(1,2),(2,3),(3,4),...], ...]
  for row in range(numOfRows):
    for column in range(numOfCols):
      # Check if there is a possibility of K in the current column (downwards),
      # Increase rows to (current row +K) and use current column, add into targetWinOption if there is no forbidden
      if row+K <= numOfRows: # in a column
        possibleWinOption = []
        for i in range(row, row+K):
          if initial_state[0][i][column] == '-':
            break; # Leave this possibility if there is a forbidden in this option
          possibleWinOption.append((i, column))
        if len(possibleWinOption) == K: # no forbidden squares
          targetWinOptions.append(possibleWinOption)
          
      # Check if there is a possibility of K in the current row (towards right),
      # Increase columns to (current column +K) and use current row, add into targetWinOption if there is no forbidden
      if column+K <= numOfCols: # in a row
        possibleWinOption = []
        for i in range(column, column+K):
          if initial_state[0][row][i] == '-':
            break; # Leave this possibility if there is a forbidden in this option
          possibleWinOption.append((row, i))
        if len(possibleWinOption) == K: # no forbidden squares
          targetWinOptions.append(possibleWinOption)
          
      # Check if there is a possibility of K diagonally (towards right-down),
      # Increase columns to (current column +K) and Increase rows to (current row +K) with each iteration, add into targetWinOption if there is no forbidden
      if column+K <= numOfCols and row+K <= numOfRows:
        possibleWinOption = []
        j = column
        for i in range(row, row+K):
          if initial_state[0][i][j] == '-':
            break;
          possibleWinOption.append((i, j))
          j += 1
        if len(possibleWinOption) == K: # Leave this possibility if there is a forbidden in this option
          targetWinOptions.append(possibleWinOption)
      
      # Check if there is a possibility of K diagonally (towards right-up),
      # Increase columns to (current column +K) and Decrease rows to (current row - K) with each iteration, add into targetWinOption if there is no forbidden
      if column+K <= numOfCols and row-K >= -1:
        possibleWinOption = []
        j = column
        for i in range(row,row-K,-1):
          if initial_state[0][i][j] == '-':
            break;
          possibleWinOption.append((i, j))
          j += 1
        if len(possibleWinOption) == K: # Leave this possibility if there is a forbidden in this option
          targetWinOptions.append(possibleWinOption)
          
  global SCORE_HASH, ZOBRIST_NUM, OPPONENT_NICKNAME
  OPPONENT_NICKNAME = opponent_nickname
  SCORE_HASH = {} # key is the Zobrist hash key (integer) for a board, value is corresponding score
  ZOBRIST_NUM = [] # [[[value for X, value for O],[value for X, value for O],...],[second row...],...]
  for row in range(numOfRows):
    possibleWinOption1 = []
    for column in range(numOfCols):
      possibleWinOption2 = [] # most inner one, values for X, O
      possibleWinOption2.append(random.randint(0,4294967296)) # for X
      possibleWinOption2.append(random.randint(0,4294967296)) # for O
      possibleWinOption1.append(possibleWinOption2)
    ZOBRIST_NUM.append(possibleWinOption1)
  
# Method 4: Here is my move
def makeMove(currentState, currentRemark, timeLimit=10000):
  start_time = time.time()
  [newState,score] = minimax_with_alpha_beta(currentState, 4, -999999999, 999999999, timeLimit, start_time, None)
  
  # score can be used to determine the remark
  newRemark = response(score, currentRemark)
  (a,b)=(-1,-1)
  # find the position of the move
  for row in range(numOfRows):
    for column in range(numOfCols):
      if not currentState[0][row][column] == newState[0][row][column]:
        (a,b)=(row,column)
  if (a,b) == (-1,-1):
    return [None, "A friendly game! I like it."] # all squares are filled
  return [[(a,b), newState], newRemark]

# Method 5: My response to your remark 
def response(score, currentRemark):
    global OPPONENT_NICKNAME
   
    if myChar != "X": score = score * (-1)
    newremark = ""
    
    # Higher the score better the chance of win of me
    
    # Negative score range, Opponent is in better situation
    # range covered: below -2000 to -500
    if score >= -1000 and score <-500:
        newremark = "Seems like you will turn out to be a strong player, " + OPPONENT_NICKNAME + "! Time for me to make a serious move."
    if score >= -2000 and score <-1000:
        newremark = OPPONENT_NICKNAME + ", Take it easy buddy, this way I might lose :(!"
    if score <-2000:
        newremark = "You certainly proved to be better than me " + OPPONENT_NICKNAME + "! I am ready for another round of game."
        
    # response of positive score rance, I am in better situation
    # range covered: 500 to above 2000
    if score >= 500 and score < 1000:
        newremark = "I haven't even gotten into form yet but looks like it's going to be a good day!"
    if score >=1000 and score < 2000:
        newremark = OPPONENT_NICKNAME + ", You might need some more focus here! :)"
    if score >=2000:
        newremark = "Better luck next time, my friend!"
    if newremark != "": return newremark
    
    # If score is not between -2000 to -500 and 500 to above 2000
    if currentRemark.find("?") !=1:
        newremark = "May be!"
        return newremark
    if "fun" in currentRemark:
        newremark = "I totally agree with you, " + OPPONENT_NICKNAME + "!"
        return newremark
    if "easy" in currentRemark:
        newremark = "Nothing is easy or tough " + OPPONENT_NICKNAME + ", continue playing!"
        return newremark
    if "win" in currentRemark:
        newremark = "How can you be so sure, " + OPPONENT_NICKNAME + "!"
        return newremark
    if "beat" in currentRemark and "you" in currentRemark:
        newremark = "Wait till the end " + OPPONENT_NICKNAME + ". Anything is possible."
        return newremark
    if "best" in currentRemark:
        newremark = "Game result will tell who is the best!"
        return newremark
    if "you" in currentRemark or "You" in currentRemark:
        newremark = "I don't think so."
        return newremark
    if "lose" in currentRemark:
        newremark = "Believe me, nobody will lose if he/she tries the best."
        return newremark
        
    # Score = 0, neutral game
    if score == 0:
        newremark = "No result might come out of this but I am happy to utilize my time doing what I love to."
    
    # Score range 10 to 50, little edge over opponent
    if score > 0 and score <= 25:
        newremark = "I have a feeling that we are going to enjoy this!"
    
    # Score range 25 to 50, little more edge over opponent, enjoying the game
    if score > 25 and score <= 50:
        newremark = "This is so much fun!!!"
    
    # Score range 50 to 200, getting heavy over opponent
    if score > 50 and score < 500:
        newremark = "May be, I am practised well in the game " + OPPONENT_NICKNAME + "!"
    
    # Score range --25 to 0, opponent getting edge over me
    if score >=-25 and score < 0:
        newremark = "Well, only time will tell " + OPPONENT_NICKNAME + ", what will happpen in the end."
    
    # Score range -50 to -25, opponant getting heavy over me
    if score >=-50 and score < -25:
        newremark = "Ah! I just do this as a time-pass."
    
    # Score range -500 to -50, opponant is moving towards win
    if score >=-500 and score <-50:
        newremark = "Looks like I can learn from you  " + OPPONENT_NICKNAME + " for the next game"
    return newremark
    
# Method 6: Calculating best move in response of current state of the boardq 
# Beta is the minimum upper bound of possible solutions
# Alpha is the maximum lower bound of possible solutions
# State[0][][] stores the board. State[1] stores X or O (char to put for the current turn). State[2] stores hash value of itself
def minimax_with_alpha_beta(currentState, depth, alpha, beta, timeLimit, start_time, hashKey):
  # get hash key of the board
  if hashKey == None:
    hashKey = getHashKey(currentState[0])
    
  # Check if score has been already there for the board
  # If not, evaluate current score of the board and save it
  global SCORE_HASH
  if hashKey in SCORE_HASH: # determine if it's already been evaluated
    currentScore = SCORE_HASH[hashKey]
  else:
    currentScore = staticEval(currentState)
    SCORE_HASH[hashKey] = currentScore
    
  # if time is getting over soomn, return currentSate and current score
  if (time.time() - start_time > timeLimit - 0.1) or (depth == 0): # 0.1 second from time limit, arbitrary, may need to change other number
    return [currentState,currentScore]
  
  # Find all possible moves on the board based on the current state along with score for the each move
  # Add current char (X or O)  to each blank square and add to possible moves
  # Each move is, [Current_State with current char, next char, score of the current state ^ position's hash key]
  global numOfRows, numOfCols, ZOBRIST_NUM
  available_moves = []
  for row in range(numOfRows):
    for column in range(numOfCols):
      if currentState[0][row][column] == ' ':
        temp = []
        temp.append(copy.deepcopy(currentState[0]))
        temp[0][row][column] = currentState[1]
        if currentState[1] == 'X':
          temp.append('O')
          temp.append(currentScore ^ ZOBRIST_NUM[row][column][0]) # append Zobrist hash key
        else:
          temp.append('X')
          temp.append(currentScore ^ ZOBRIST_NUM[row][column][1]) # append Zobrist hash key
        available_moves.append(temp)
  
  # If possible moves are none, return currentSate and current score
  if len(available_moves) == 0:
    return [currentState,currentScore]
  
  
  if currentState[1] == 'X': # select maximum children
    v = alpha
    newState = currentState
    for available_state in available_moves:
      [tempState,tempScore] = minimax_with_alpha_beta(available_state[0:2],depth-1,v,beta,timeLimit,start_time,available_state[2])
      if tempScore > v: # greater than previous maximum lower bound 
        v = tempScore
        newState = available_state[0:2]
      if v >= beta: # greater than or equal to upper bound
        break
    return [newState,v]
  else: # select minimum children in case of 'O'
    v = beta
    newState = currentState
    for available_state in available_moves:
      [tempState,tempScore] = minimax_with_alpha_beta(available_state[0:2],depth-1,alpha,v,timeLimit,start_time,available_state[2])
      if tempScore < v: # smaller than previous maximum upper bound 
        v = tempScore
        newState = available_state[0:2]
      if v <= alpha: # smaller than or equal to lower bound
        break
    return [newState,v]

# Method 7: Calculating hashkey of the given state of the board
def getHashKey(board):
  global numOfRows, numOfCols, ZOBRIST_NUM
  val = 0
  for row in range(numOfRows):
    for column in range(numOfCols):
      piece = None
      if (board[row][column] == "X"):
        piece = 0
      if (board[row][column] == "O"):
        piece = 1
      if (piece != None):
        val = val ^ ZOBRIST_NUM[row][column][piece]
  return val
  
# Method 8: Calculating score of the current state
def staticEval(state):
  win_list = [] # has the form [[X,X,O, ,...],[O,X,O,...],...]
  global targetWinOptions
  for win_combination in targetWinOptions:
    temp = []
    for (a,b) in win_combination:
      temp.append(state[0][a][b])
    win_list.append(temp)
  score = 0
  global K
  for win_combination in win_list:
    x_num = win_combination.count('X')
    if x_num > 0:
      first_x_index = win_combination.index('X')
    o_num = win_combination.count('O')
    if o_num > 0:
      first_o_index = win_combination.index('O')
    
    if x_num > 0:
      loop = K
      while loop>1:
        count = 0
        for char in win_combination:
            if char == 'X':
                count +=1
            elif char == '0':
                count = 0 
        if count == loop:
            score += 10**(loop-1)
            break
        loop -=1
      if x_num == 1 and o_num == 0:
        score += 1
    if o_num > 0:
      loop = K-1
      while loop>1: 
        count = 0
        for char in win_combination:
            if char == 'O':
                count +=1
            elif char == 'X':
                count = 0 
        if count == loop:
            score -= 10**(loop-1)
            break
        loop -=1
      if o_num == 1 and x_num == 0:
        score -= 1
  return score
