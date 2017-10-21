# AStar.py
# A* Search of a problem space.
# Ver 0.1, October 19, 2017.
# Usage:
# python3 AStar.py EightPuzzleWithHeuristics h_euclidean puzzle2a


import sys
from priorityq import PriorityQ


if sys.argv == [''] or len(sys.argv) < 3:
    import EightPuzzleWithHeuristics as Problem
    CHOSEN_HEURISTIC = 'h_manhattan'
    INITIAL_STATE =  Problem.CREATE_INITIAL_STATE()
    h_score_fn = Problem.HEURISTICS[CHOSEN_HEURISTIC]  # scoring function

else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    CHOSEN_HEURISTIC = sys.argv[2]
    initial_state_file = importlib.import_module(sys.argv[3])
    INITIAL_STATE = initial_state_file.CREATE_INITIAL_STATE()
    h_score_fn = Problem.HEURISTICS[CHOSEN_HEURISTIC]  # scoring function


print("\nWelcome to A Star Search")
COUNT = None
BACKLINKS = {}

def runAStar():
    initial_state = INITIAL_STATE
    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    AStar(initial_state)
    print(str(COUNT) + " states examined.")


def AStar(initial_state):
    # print("In RecDFS, with depth_limit="+str(depth_limit)+", current_state is ")
    # print(Problem.DESCRIBE_STATE(current_state))
    global COUNT, BACKLINKS

    #Tracks most efficient previous step
    BACKLINKS[initial_state] = None

    #already evaluated states
    CLOSED = []

    #currently discovered, not yet evaluated states
    OPEN = PriorityQ()

    #Calculate F, G, H scores
    initialize_scores(initial_state)

    #Only initial node is known as of now
    OPEN.insert(initial_state, F_SCORE[initial_state])

    while OPEN.isEmpty() !=True:
        S = OPEN.deletemin()
        CLOSED.append(S)

        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            backtrace(S)
            return #FOUND GOAL

        COUNT += 1
        if (COUNT % 32)==0:
#        if True:
            # print(".",end="")
#            if (COUNT % 128*128)==0:
            if True:
                print("COUNT = " + str(COUNT))
                #print("len(OPEN)=" + str(len(OPEN))) #PriorityQ OPEN doesn't have len()
                print("len(CLOSED)=" + str(len(CLOSED)))


        for op in Problem.OPERATORS:
            if op.precond(S):
                new_state = op.state_transf(S)
                if not occurs_in(new_state, CLOSED): #ignore already evaluated neighbors

                    #find tentative score of neighbor
                    tentative_g_score = G_SCORE[S] + 1

                    if new_state not in G_SCORE: #Default INFINITY
                        BACKLINKS[new_state] = S   #First known path to new_state
                    elif  tentative_g_score >= G_SCORE[new_state]:
                        continue #current path is not the best path to the neighbor
                    else:
                        BACKLINKS[new_state] = S  #Found better path to new_State

                    G_SCORE[new_state] = tentative_g_score
                    F_SCORE[new_state] = G_SCORE[new_state] + h_score_fn(new_state)

                    # discovered a new State
                    if not OPEN.__contains__(new_state):
                        OPEN.insert(new_state, F_SCORE[new_state])

                    # print(Problem.DESCRIBE_STATE(new_state))
            #print(OPEN)

    #Failure, if goal_test has not succeeded until now
    print("COULD NOT FIND GOAL")
    return


def initialize_scores(start_state):
    reset_Scores()
    G_SCORE[start_state] = 0
    H_SCORE[start_state] = h_score_fn(start_state)
    F_SCORE[start_state] = H_SCORE[start_state]

def reset_Scores():
    """
    Reset just in case run AStar multiple times
    """
    G_SCORE = {}
    F_SCORE = {}
    H_SCORE = {}

def print_state_list(name, lst):
    print(name + " is now: ", end='')
    for s in lst[:-1]:
        print(str(s), end=', ')
    print(str(lst[-1]))

def backtrace(S):
    global BACKLINKS

    path = []
    while S:
        path.append(S)
        # print("In backtrace, S is now: "+str(S))
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    return path

def occurs_in(s1, lst):
    for s2 in lst:
        if s1 == s2: return True
    return False

if __name__ == '__main__':
    runAStar()