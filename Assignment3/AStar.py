'''Name    = Vaibhavi Rangarajan, UWNetID = vaibhavi
'''
# Astar.py, April 2017
# Based on ItrDFS.py, Ver 0.4a, October 14, 2017.

# A* Search of a problem space.
# The Problem should be given in a separate Python
# file using the "QUIET" file format.
# See the TowerOfHanoi.py example file for details.
# Examples of Usage:

# A small change was made on Oct. 14, so that backtrace
# uses None as the BACKLINK value for the initial state,
# just as in ItrDFS.py, rather than using -1 as it did
# in an earlier version.

# python3 AStar.py EightPuzzleWithHeuristics h_manhattan

import sys
from priorityq import PriorityQ

# DO NOT CHANGE THIS SECTION
if sys.argv == [''] or len(sys.argv) < 2:
    import EightPuzzleWithHeuristics as Problem
    heuristics = lambda s: Problem.HEURISTICS['h_manhattan'](s)

else:
    import importlib
    Problem = importlib.import_module(sys.argv[1])
    heuristics = lambda s: Problem.HEURISTICS[sys.argv[2]](s)


print("\nWelcome to AStar")
COUNT = None
BACKLINKS = {}

#Score Dictionaries
# If state node is not present in G or F score, treat it as Infinity by default
F_SCORE = {} #Start to Goal (Known + Estimated)
G_SCORE = {} #Start to Node (Known)
H_SCORE = {} #Node to Goal (Estimated)


# DO NOT CHANGE THIS SECTION
def runAStar():
    initial_state = Problem.CREATE_INITIAL_STATE()

    #Use an externally specified initial state
    if len(sys.argv)>3:
        initial_state_file = importlib.import_module(sys.argv[3])
        initial_state = initial_state_file.CREATE_INITIAL_STATE()

    print("Initial State:")
    print(initial_state)
    global COUNT, BACKLINKS
    COUNT = 0
    BACKLINKS = {}
    path, name = AStar(initial_state)
    print(str(COUNT) + " states examined.")
    return path, name


# A star search algorithm
def AStar(initial_state):
    global COUNT, BACKLINKS
    OPEN = PriorityQ()                  #currently discovered, not yet evaluated states
    CLOSED = []                         #already evaluated states
    BACKLINKS[initial_state] = None     #Tracks most efficient previous step

    #Calculate F, G, H scores for Starting state
    initialize_scores(initial_state)

    #Only one state is known as of now
    OPEN.insert(initial_state, F_SCORE[initial_state])

    while OPEN.isEmpty() !=True:
        S, priority = OPEN.deletemin()
        while S in CLOSED:
            S = OPEN.deletemin()
        CLOSED.append(S)

        # DO NOT CHANGE THIS SECTION: beginning
        if Problem.GOAL_TEST(S):
            print(Problem.GOAL_MESSAGE_FUNCTION(S))
            path = backtrace(S)
            return path, Problem.PROBLEM_NAME
            # DO NOT CHANGE THIS SECTION: end

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

                    elif  tentative_g_score <= G_SCORE[new_state]:
                        BACKLINKS[new_state] = S  # Found better path to new_State

                    else: continue #current path is not the best path to the neighbor

                    G_SCORE[new_state] = tentative_g_score
                    F_SCORE[new_state] = G_SCORE[new_state] + h_score_fn(new_state)

                    # Delete previous F-score in PriorityQ if it exists
                    if OPEN.__contains__(new_state):
                        OPEN.remove(new_state)

                    #Update PriorityQ with new priority
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
    Reset just in case AStar is run multiple times
    """
    G_SCORE = {}
    F_SCORE = {}
    H_SCORE = {}

def h_score_fn(S):
    return heuristics(S)

def occurs_in(s1, lst):
    for s2 in lst:
        if s1 == s2: return True
    return False


# DO NOT CHANGE
def backtrace(S):
    global BACKLINKS
    path = []
    while S:
        path.append(S)
        S = BACKLINKS[S]
    path.reverse()
    print("Solution path: ")
    for s in path:
        print(s)
    print("\nPath length = " + str(len(path) - 1))
    return path


if __name__ == '__main__':
    path, name = runAStar()