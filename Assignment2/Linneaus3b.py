# Linneus3b.py
# Implements storage and inference on an ISA hierarchy
# This Python program goes with the book "The Elements of Artificial
# Intelligence".
# This version runs under Python 3.x.

# Steven Tanimoto
# (C) 2012. updated 2017 to use Python's defaultdict class.

# The ISA relation is represented using a dictionary, ISA.
# There is a corresponding inverse dictionary, INCLUDES.
# Each entry in the ISA dictionary is of the form
#  ('turtle' : ['reptile', 'shelled-creature'])

# This version includes a testing option to help during development
# of the special feature required in Assignment 2 of CSE 415 during
# Autumn Quarter, 2017 at the University of Washington.
# The test option was implemented by Connor Schenck.

from re import *  # Loads the regular expression module.
from collections import defaultdict
import pprint as pp

###########################################################
#KNOWLEDGE REPRESENTATION

###########################################################

ISA = defaultdict(list)
INCLUDES = defaultdict(list)
ARTICLES = defaultdict(str)
SYNONYMS = defaultdict(list)

def reset():
    global ISA, INCLUDES, ARTICLES, SYNONYMS
    ISA = defaultdict(list)
    INCLUDES = defaultdict(list)
    ARTICLES = defaultdict(str)
    SYNONYMS = defaultdict(list)

def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    cat1 = get_root_synonym(category1)
    return ISA[cat1]


def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    cat1 = get_root_synonym(category1)
    return INCLUDES[cat1]


def isa_test1(category1, category2):
    'Returns True if category 1 is a direct subset of category 2'
    cat1 = get_root_synonym(category1)
    cat2 = get_root_synonym(category2)
    'Returns True if category 2 is (directly) on the list for category 1.'
    return get_isa_list(cat1).__contains__(cat2)


def isa_test(category1, category2, depth_limit=10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    cat1 = get_root_synonym(category1)
    cat2 = get_root_synonym(category2)

    if category1 == category2:
        return True
    if cat1 == cat2:
        return True
    if isa_test1(cat1, cat2):
        return True
    if depth_limit < 2:
        return False
    for intermediate_category in get_isa_list(cat1):
        if isa_test(intermediate_category, cat2, depth_limit - 1):
            return True
    return False


def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()


def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    return ARTICLES[noun]


def store_synonym(category1, category2):
    global SYNONYMS
    #avoid repeated addition for self synonym
    if category1 == category2 and category1 not in SYNONYMS:
        SYNONYMS[category1].append(category1)
        return
    SYNONYMS[category1].append(category2)


def get_synonyms_list(noun):
    root_noun = get_root_synonym(noun)
    return SYNONYMS[root_noun]


def get_root_synonym(noun):
    for root_noun, synonyms in SYNONYMS.items():
        if noun in synonyms: #list/ set
            #print("Accessed Root", root_noun)
            return root_noun
    print("No root", noun)
    return



def is_graph_cyclic(category1, category2):
    'Returns true if the statement category1 IS A category2 creates a cycle (antisymmetry check)'
    if isa_test(category2, category1): #
        return True
    else: return False


def store_isa_fact(category1, category2, verbose=False):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    cat1 = get_root_synonym(category1)
    cat2 = get_root_synonym(category2)

    # Check if Cycle detected
    is_cyclic = is_graph_cyclic(cat1, cat2)

    if verbose:
        print("Will graph become cyclic ? ", is_cyclic)

    if not is_cyclic:
        ISA[cat1].append(cat2)
        INCLUDES[cat2].append(cat1)
        print("I understand.")
        return

    else:
        chosen_noun = eliminate_cycle(cat1, cat2, verbose)
        eq_names = get_synonyms_list(chosen_noun)
        print("I infer that", listify(eq_names), "are all names for the same thing and I'll call it", chosen_noun+".")
        return

def listify(names):
    s=""
    if len(names) < 2:
       print("Not enough Synonyms!")
       return

    last = names[-1]
    for n in names[:-1]:
        s += n + ", "
    s+= "and "+last
    return s

def eliminate_cycle(category1, category2, verbose = False):
    'Check if there is a path between 2 to 1, and then eliminate the cycle'
    cat1 = get_root_synonym(category1)
    cat2 = get_root_synonym(category2)

    #Check there is no cycle to eliminate
    if not isa_test(cat2, cat1):
        print("ERROR: No cycle to eliminate!")
        return

    if verbose:
        print('Eliminating Cycle')

    #Paths exist from Category2 to Category 1 for the cycle
    affected_nodes = get_affected_nodes(cat2, cat1, verbose)
    if len(affected_nodes) < 2:
        print("ERROR: No path exists")

    return recreate_graph(cat1, cat2, affected_nodes, verbose)

def get_affected_nodes(start_category, end_category, verbose = False):
    'Returns UNORDERED list of elements on all paths from category 1 until category 2'
    affected_nodes=[]
    start = get_root_synonym(start_category)
    end = get_root_synonym(end_category)

    paths = find_all_paths(start, end)
    affected_nodes = find_nodes_on_any_paths(paths)

    if verbose == True:
        print("\nALL Paths between", start_category, 'and', end_category, '=\n', paths)
        print("\nALL affected nodes between ", start_category, 'and',end_category,'=\n', affected_nodes)

    return affected_nodes


def find_all_paths(start, end, path=[]):
    'find all paths from start_node to end_node in graph'
    path = path + [start]
    if start == end:
        return [path]
    #no possible movement
    if ISA[start] ==[]:
        return []

    paths = [] #list of paths
    for vertex in ISA[start]:
        if vertex not in path:
            extended_paths = find_all_paths(vertex, end, path)
            for p in extended_paths:
                paths.append(p)
    return paths


def find_nodes_on_any_paths(paths):
    'Returns unordered list of all nodes that are on some path from START to END'
    flat_list = [node for path in paths for node in path]
    unique_flat_list = list(set(flat_list))
    return unique_flat_list


def recreate_graph(cat1, cat2, equivalent_nouns, verbose=False):
    'Returns single chosen noun after removing equivalent nouns from the ISA, SYNONYMS and INCLUDES KEYS and VALUES'
    global SYNONYMS, ISA, INCLUDES

    #Arbitrary choice of cat2 as chosen key for synonyms
    chosen_noun = cat2
    equivalent_nouns.remove(chosen_noun)
    if verbose:
        print("\nChosen Noun = ", chosen_noun)
        print("Equivalent Nouns to remove = ", equivalent_nouns)

    #Combine all entries of equivalent nouns under chosen noun
    combine_keys("SYNONYMS", equivalent_nouns, chosen_noun, verbose)
    combine_keys("INCLUDES", equivalent_nouns, chosen_noun, verbose)
    combine_keys("ISA", equivalent_nouns, chosen_noun, verbose)

    #Remove mentions of ALL synonyms of chosen noun from ISA, INCLUDES graphs
    eq_names = get_synonyms_list(chosen_noun)
    clean_dict("ISA", eq_names, chosen_noun, verbose)
    clean_dict("INCLUDES", eq_names, chosen_noun, verbose)

    return chosen_noun

def combine_keys(dict_name, eq_keys, chosen_key, verbose=False):
    'Combines all entries for equivalent keys under chosen key in dictionary d'
    global ISA, INCLUDES, SYNONYMS
    d = defaultdict(list)
    if dict_name =="ISA":
        d = ISA
    elif dict_name =="INCLUDES":
        d = INCLUDES
    elif dict_name =="SYNONYMS":
        d = SYNONYMS
    else: print("Invalid Dictionary name")

    if chosen_key in eq_keys:
        eq_keys.remove(chosen_key)

    chosen_values =[]
    #Remove all traces of equivalent nodes
    for k in eq_keys:
        vals = d.pop(k)
        chosen_values.extend(vals)

    existing_values = d.pop(chosen_key,[])
    new_values = existing_values + chosen_values
    d[chosen_key] = list(set(new_values))

    if verbose:
        print("\nCOMBINED DICTIONARY = ", dict_name)
        pp.pprint(d)

    #Change Global Dictionary
    if dict_name =="ISA":
        ISA = d
    elif dict_name =="INCLUDES":
        INCLUDES = d
    elif dict_name == "SYNONYMS":
        SYNONYMS = d


def clean_dict(dict_name,eq_names,chosen_key, verbose=False):
    'Cleans up ISA and INCLUDES to ensure no mention of synonyms in VALUES instead of chosen noun'
    global ISA, INCLUDES

    d = defaultdict(list)
    if dict_name =="ISA":
        d = ISA
    elif dict_name =="INCLUDES":
        d = INCLUDES
    else:
        print("Invalid Dictionary name")
        return

    if len(eq_names) < 1: #eq_names is chosen_key synonyms, excluding chosen_key
        return #No need to replace anything

    new_d = defaultdict(list)
    for key, values in d.items():
        new_values = [chosen_key if x in eq_names else x for x in values]
        new_values = list(set(new_values))
        new_d[key] = new_values

    #chosen_key should not appear in ISA[chosen_key], INCLUDES[chosen_key](Symmetry is implied)
    vals = new_d.pop(chosen_key)
    if chosen_key in vals and len(vals) >1:
        vals.remove(chosen_key)
        new_d[chosen_key] = vals

    #Change Global Dictionary
    if dict_name =="ISA":
        ISA = new_d
    elif dict_name =="INCLUDES":
        INCLUDES = new_d


    if verbose:
        print("\nCLEANED DICTIONARY  = ", dict_name)
        if dict_name =="ISA":
            pp.pprint(ISA)
        else:
            pp.pprint(INCLUDES)


##############################################################
#Controlling Logic
##############################################################

def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    print('Type \'test\' to run tests.')
    while True:
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        if info == 'test':
            test()
        if info == '\n':
            return
        else:
            process(info)

# Some regular expressions used to parse the user sentences:
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
tell_me_about_pattern = compile(r"^Tell me what you know about\s+(\'|\")([-\w]+)(\'|\")\s*,*\s*with\s+justification.|!|\?*", IGNORECASE)


def process(info):
    'Handles the user sentence, matching and responding.'
    #ASSERTION
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()

        a1 = items[0]
        a2 = items[2]
        noun1 = items[1]
        noun2 = items[3]

        store_article(noun1, a1)
        store_synonym(noun1,noun1) #Each is a synonym of itself

        if noun1 == noun2:
            print("I understand. It is obvious.")
            return

        store_article(noun2, a2)
        store_synonym(noun2, noun2)  # Each noun is a synonym of itself

        #Store fact and prints response
        store_isa_fact(noun1, noun2, verbose = True)


    #QUERY
    result_match_object = query_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        noun1 = items[1]
        noun2 = items[3]

        root_noun1 = get_root_synonym(noun1)
        root_noun2 = get_root_synonym(noun2)

        answer = isa_test(root_noun1, root_noun2)
        if answer:
            print("Yes, it is.")
        else:
            print("No, as far as I have been informed, it is not.")
        return

    #WHAT IS A ___
    result_match_object = what_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        supersets = get_isa_list(items[1])
        subsets = get_includes_list(items[1])
        eq_words = get_synonyms_list(items[1])
        eq_words.remove(items[1])

        if supersets != []:
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        elif subsets != []:
            first = subsets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
            return
        elif len(eq_words) >=1:
            print(a1 + " " + items[1] + " means the same thing as " + listify(eq_words) + ".")
            return
        else:
            print("I don't know.")
            return


    #WHY IS __  A __
    result_match_object = why_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]):
            print("But that's not true, as far as I know!")
        else:
            answer_why(items[1], items[3])
        return


    #TELL ME ABOUT
    result_match_object = tell_me_about_pattern.match(info)
    if result_match_object !=None:
        items = result_match_object.groups()

        noun = items[1]
        a1 = get_article(noun)

        if noun ==None:
            return

        root = get_root_synonym(noun)
        supersets = get_isa_list(root)
        subsets = get_includes_list(root)
        eq_words = get_synonyms_list(root)
        eq_words.remove(noun)

        #Explain all synonyms
        if len(eq_words) >=1:
            print(a1 + " " + noun + " means the same thing as " + listify(eq_words) + ".")

        #Tell more about ancestors
        if supersets != []:
            isa_bfs(root)

        #Tell more about successors
        if subsets != []:
            includes_bfs(root)

        #No ancestors or successors
        elif supersets ==[]  and subsets==[]:
            a= get_article(noun)
            print(a,noun,"is",a,noun+".")
            return

        print("That's all I know about \'%s\'."% noun)
        return


    print("I do not understand. You entered: ")
    print(info)

###################################################
#PROCESSING HELPER FUNCTIONS

###################################################

def answer_why(x, y):
    'Handles the answering of a Why question.'
    root1 = get_root_synonym(x)
    root2 = get_root_synonym(y)

    if x == y:
        print("Because they are identical")
    if root1 == root2:
        print("Because",x, "is another name for",y+".")
        return

    prefix_phrase = get_phrase(x, root1)
    if prefix_phrase !="":
        prefix_phrase = prefix_phrase + ", and "

    suffix_phrase = get_phrase(y,root2)

    if isa_test1(x, y):
        print("Because you told me that.")
        return

    print("Because " + prefix_phrase + report_chain(x, y)[:-1] + suffix_phrase +".")
    return


def get_phrase(noun, root_noun):
    if noun == root_noun:
        return ""
    else:
        return noun + " is another name for " + root_noun

from functools import reduce

def report_chain(x, y):
    'Returns a phrase that describes a chain of facts.'
    chain = find_chain(x, y)
    all_but_last = chain[0:-1]
    last_link = chain[-1]
    main_phrase = reduce(lambda x, y: x + y, map(report_link, all_but_last))
    last_phrase = "and " + report_link(last_link)
    new_last_phrase = last_phrase[0:-2] + '.'
    return main_phrase + new_last_phrase


def report_link(link):
    'Returns a phrase that describes one fact.'
    x = link[0]
    y = link[1]
    a1 = get_article(x)
    a2 = get_article(y)
    return a1 + " " + x + " is " + a2 + " " + y + ", "


def find_chain(x, z):
    'Returns a list of lists, which each sublist representing a link.'
    if isa_test1(x, z):
        return [[x, z]]
    else:
        for y in get_isa_list(x):
            if isa_test(y, z):
                temp = find_chain(y, z)
                temp.insert(0, [x, y])
                return temp


#Explore the Hierarchy upwards (Ancestors)
def isa_bfs(x):
    EXPLORED=[]
    queue = [x]
    a1 = get_article(x).capitalize()

    while queue:
        y = queue.pop(0)
        if y not in EXPLORED:
            #Process New Node
            if y !=x:
                a2 = get_article(y)
                if isa_test1(x, y):
                    print(a1,x ,"is", a2,y+"; you told me that directly.")
                else:
                    print(a1, x, "is", a2, y+", because",report_chain(x,y).lower())
            EXPLORED.append(y)
            L = get_isa_list(y)
            for ancestor in L:
                if ancestor not in EXPLORED:
                    queue.append(ancestor)

#Explore the hierarchy downwards (Successors)
def includes_bfs(x):
    EXPLORED=[]
    queue = [x]
    a1= get_article(x).capitalize()

    while queue:
        y = queue.pop(0)
        if y not in EXPLORED:
            a2=get_article(y)
            #Process New Node
            if y !=x:
                if isa_test1(y,x):
                    print(a1,x ,"is something more general than", a2,y+", because",a2,y,"is",a1.lower(),x+".")
                else:
                    print(a1, x, "is something more general than", a2, y+", because",report_chain(y,x))

            EXPLORED.append(y)
            L = get_includes_list(y)
            for successor in L:
                if successor not in EXPLORED:
                    queue.append(successor)
    return

########################################################
#TEST CASES
########################################################

CASE1 = [
    ("A turtle is a reptile.", None),
    ("A turtle is a shelled-creature.", None),
    ("A reptile is an animal.", None),
    ("An animal is a thing.", None),
    ("Is a turtle a reptile.", ["Yes, it is."]),
    ("Is a turtle an animal.", ["Yes, it is."]),
    ("What is a turtle?", ["A turtle is a reptile."]),
    ("Why is a turtle an animal?", ["Because a turtle is a reptile, and a reptile is an animal."]),
    ("Why is an animal a reptile?", ["But that's not true, as far as I know!"]),
    ("Tell me what you know about \'turtle\', with justification.", [
        "A turtle is a reptile; you told me that directly.",
        "A turtle is a shelled-creature; you told me that directly.",
        "A turtle is an animal, because a turtle is a reptile and a reptile is an animal.",
        "A turtle is a thing, because a turtle is a reptile, a reptile is an animal, and an animal is a thing.",
        "That's all I know about \'turtle\'."]),
]

CASE2 = [
    ("A BugsBunny is a cartoon.", None),
    ("A DaffyDuck is a cartoon.", None),
    ("A BugsBunny is a rabbit.", None),
    ("A DaffyDuck is a duck.", None),
    ("A duck is a bird.", None),
    ("A bird is an animal.", None),
    ("A rabbit is a mammal.", None),
    ("A mammal is an animal.", None),
    ("Is a BugsBunny an animal?", ["Yes, it is."]),
    ("Is a DaffyDuck a rabbit?", ["No, as far as I have been informed, it is not."]),
    ("Tell me what you know about \'DaffyDuck\', with justification.", [
        "A DaffyDuck is a cartoon; you told me that directly.",
        "A DaffyDuck is a duck; you told me that directly.",
        "A DaffyDuck is a bird, because a DaffyDuck is a duck and a duck is a bird",
        "A DaffyDuck is an animal, because a DaffyDuck is a duck, a duck is a bird, and a bird is an animal.",
        "That's all I know about \'DaffyDuck\'."]),
    ("Tell me what you know about \'rabbit\', with justification.", [
        "A rabbit is a mammal; you told me that directly.",
        "A rabbit is an animal, because a rabbit is a mammal and a mammal is an animal.",
        "A rabbit is something more general than a BugsBunny, because a BugsBunny is a rabbit.",
        "That's all I know about \'rabbit\'."]),
]

def test():
    TESTS = [CASE1, CASE2]
    import sys
    import io
    old_stdout = sys.stdout
    new_stdout = io.StringIO()

    for i, case in enumerate(TESTS):
        print("======== TEST %d =========" % i)
        reset()
        for inp, out in case:
            print("         INPUT: %s" % inp)
            sys.stdout = new_stdout
            process(inp)
            sys.stdout = old_stdout
            lines = [x.strip() for x in new_stdout.getvalue().split("\n") if x.strip()]
            new_stdout = io.StringIO()
            if out is not None:
                for l in lines:
                    print("   YOUR OUTPUT: %s" % l)
                for l in out:
                    print("CORRECT OUTPUT: %s" % l)
                print("")
        print("")

#########################################################
# FUNCTION CALLS
#########################################################
# Launch the program.
if __name__ == "__main__":
    linneus()