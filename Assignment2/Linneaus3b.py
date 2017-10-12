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

ISA = defaultdict(list)
INCLUDES = defaultdict(list)
ARTICLES = defaultdict(str)


def reset():
    global ISA, INCLUDES, ARTICLES
    ISA = defaultdict(list)
    INCLUDES = defaultdict(list)
    ARTICLES = defaultdict(str)

def store_isa_fact(category1, category2):
    'Stores one fact of the form A BIRD IS AN ANIMAL'
    # That is, a member of CATEGORY1 is a member of CATEGORY2
    ISA[category1].append(category2)
    INCLUDES[category2].append(category1)


def get_isa_list(category1):
    'Retrieves any existing list of things that CATEGORY1 is a'
    return ISA[category1]


def get_includes_list(category1):
    'Retrieves any existing list of things that CATEGORY1 includes'
    return INCLUDES[category1]


def isa_test1(category1, category2):
    'Returns True if category 2 is (directly) on the list for category 1.'
    return get_isa_list(category1).__contains__(category2)


def isa_test(category1, category2, depth_limit=10):
    'Returns True if category 1 is a subset of category 2 within depth_limit levels'
    if category1 == category2: return True
    if isa_test1(category1, category2): return True
    if depth_limit < 2: return False
    for intermediate_category in get_isa_list(category1):
        if isa_test(intermediate_category, category2, depth_limit - 1):
            return True
    return False


def store_article(noun, article):
    'Saves the article (in lower-case) associated with a noun.'
    ARTICLES[noun] = article.lower()


def get_article(noun):
    'Returns the article associated with the noun, or if none, the empty string.'
    return ARTICLES[noun]


def linneus():
    'The main loop; it gets and processes user input, until "bye".'
    print('This is Linneus.  Please tell me "ISA" facts and ask questions.')
    print('For example, you could tell me "An ant is an insect."')
    print('Type \'test\' to run tests.')
    while True:
        info = input('Enter an ISA fact, or "bye" here: ')
        if info == 'bye': return 'Goodbye now!'
        if info == 'test':
            #test()
            print("")
        else:
            process(info)


# Some regular expressions used to parse the user sentences:
assertion_pattern = compile(r"^(a|an|A|An)\s+([-\w]+)\s+is\s+(a|an)\s+([-\w]+)(\.|\!)*$", IGNORECASE)
query_pattern = compile(r"^is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
what_pattern = compile(r"^What\s+is\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)
why_pattern = compile(r"^Why\s+is\s+(a|an)\s+([-\w]+)\s+(a|an)\s+([-\w]+)(\?\.)*", IGNORECASE)

#pattern_str= "^(Tell)\s+(me)\s+(what)\s+(you)\s+(know)\s+(about)\s+(\'|\")[-\w]+(\'|\")\s*(,)*\s*(with)\s+(justification)(.|!|\?)*$"
tell_me_about_pattern = compile(r"^Tell\s+me\s+what\s+you\s+know\s+about\s+(\'|\")([-\w]+)(\'|\")\s*,*\s*with\s+justification.|!|\?*$", IGNORECASE)

def process(info):
    'Handles the user sentence, matching and responding.'
    #ASSERTION
    result_match_object = assertion_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        store_article(items[1], items[0])
        store_article(items[3], items[2])
        store_isa_fact(items[1], items[3])
        print("I understand.")
        return

    #QUERY
    result_match_object = query_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        answer = isa_test(items[1], items[3])
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
        if supersets != []:
            first = supersets[0]
            a1 = get_article(items[1]).capitalize()
            a2 = get_article(first)
            print(a1 + " " + items[1] + " is " + a2 + " " + first + ".")
            return
        else:
            subsets = get_includes_list(items[1])
            if subsets != []:
                first = subsets[0]
                a1 = get_article(items[1]).capitalize()
                a2 = get_article(first)
                print(a1 + " " + items[1] + " is something more general than " + a2 + " " + first + ".")
                return
            else:
                print("I don't know.")
        return

    #WHY IS __  A __
    result_match_object = why_pattern.match(info)
    if result_match_object != None:
        items = result_match_object.groups()
        if not isa_test(items[1], items[3]):
            print("But that's not true, as far as I know!"
                  )
        else:
            answer_why(items[1], items[3])
        return

    #TELL ME ABOUT
    result_match_object = tell_me_about_pattern.match(info)
    if result_match_object !=None:
        items = result_match_object.groups()
        noun = items[1]

        supersets = get_isa_list(noun)
        if supersets != []:
            isa_bfs(noun)

        subsets = get_includes_list(noun)
        if subsets != []:
            includes_bfs(noun)

        if supersets ==[]  and subsets==[]:
            print("I don't know")
            return

        print("That's all I know about \'%s\'."% noun)
        return


    print("I do not understand.  You entered: ")
    print(info)

def answer_why(x, y):
    'Handles the answering of a Why question.'
    if x == y:
        print("Because they are identical.")
        return
    if isa_test1(x, y):
        print("Because you told me that.")
        return
    print("Because " + report_chain(x, y))
    return


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


def answer_tell_me_more(x, y, type="parent"):
    if x == y:
        print("Because they are identical.")
        return

    if type =="parent":
        print("you told me that directly.")

    elif isa_test1(x, y):
        print("")

    if type=="child":
        print()

        return

    print(", because " + report_chain(x, y))
    return


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

#isa_bfs("rabbit")
