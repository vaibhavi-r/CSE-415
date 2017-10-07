from random import choice
from re import *

######################################################################################################
"""KNOWLEDGE MAP
- Lists of People, Places, Foods, Colors, Drinks, Greetings and Excuses etc.
- Count Variables Initialization for Cyclic Responses
- Lists of Random and (Default) Cyclic Response templates
"""
# KNOWLEDGE MAP
# Everything Ethel knows before the conversation

GOODBYE_WORDS = ['Bye', 'Ciao', 'Sayonara', 'Goodbye', 'Goodnight', 'bye', 'See ya later', 'See ya']
GREETING_WORDS = ['good morning', 'hey', 'hi', 'hello', "hullo", "aloha", "whats up", "wassup"]

HOBBY_TRIGGERS = ['hobby', 'hobbies', 'like']
HOBBIES = ['knit', 'kick butt', 'karate chop and do squats', 'volunteer', 'sing', 'dance creepily', 'meditate']

PLACE_TRIGGERS = ['where', 'place', 'gym', 'hospital', 'home']
PLACES = ['my house', 'the hospital', 'the club', 'prison', 'the Statue of Liberty', 'Mount Everest', 'the gym',
          'the Museum of Modern Art', 'hell', "the White House", "Earth", 'the bathtub']

FOODS = ['pizza', 'burgers', 'cake', 'cookies', 'ice-cream', 'potatoes', 'carrots', 'baby tacos' 'quiche']
PEOPLE = ['Nelson Mandela', 'Elmo the Puppet', 'Queen Elizabeth II', 'Dwayne The Rock Johnson', 'Adele']
COLORS = ['red', 'green', 'blue', 'purple', 'teal', 'yellow', 'pink', 'black', 'white', 'lavender']
DRINKS = ["Ol' fashioned", "Vodka martini", "Pina Colada", "Olive Oil", "Orange juice", "Water",
          "Warm milk", "Mango milkshake", "Seltzer water"]

EXCUSES = ["my knees aren't working since 1942.",
           "I hate Sun-days.. Get it? You don't get it. Let it be.",
           'the bird ate all the breadcrumbs I had.',
           "... just because.. I cannot say. You would not understand.",
           "the war happened and nothing was the same.",
           "I died and came back to life just recently."]

TIME = ['year', 'month', 'week', 'time', 'hour', 'minute', 'morning', 'afternoon', 'night',
        'evening']  # Use with Last, upcoming
DAYS_OF_WEEK = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

###################################################################################################
"""
PRODUCTION RULE BASE
Includes 34 Rules which are Bundled into RULE SETS / functions for ease of response.

Cyclic response generation = PR27, PR28, PR28, PR29, PR30, PR31
Random response generation = PR32, PR33
Retriving old memory       = PR34

"""
######################################################################################################
# RULE BASE
# Rules Ethel uses to respond
# NOTE: Multiple rules bundled into functions to test at once.

# EMPTY INPUT
"""PR1: Check if there's an empty string. Respond with """
def empty_wordlist_rule(wordlist, mapped_wordlist):
    if wordlist[0] == '':
        return "Hello darkness, my old friend. I've come to talk with you again. Say something, please?"
    else:
        return False


# CHECK FOR GREETING
"""PR2: If User says a 1 word Greeting keyword - e.g. Hello, : Respond with Random Response """
"""PR3: If User says a 2 word Greeting- e.g. Good Morning : Respond with Grumpy response of not liking mornings"""
def check_for_greeting_rule_set(wordlist, mapped_wordlist):
    #PR2
    if wordlist[0] in GREETING_WORDS:
        happy_greeting = choice(GREETING_WORDS).capitalize() + "! " + give_super_random_opinion_and_ask()
        return happy_greeting

    #PR3
    if len(wordlist) > 1 and wordlist[0] + " " + wordlist[1] in GREETING_WORDS:
        annoyed_greeting = choice(GREETING_WORDS).capitalize() + "! I don't like mornings because " + choice(EXCUSES)
        return annoyed_greeting
    return False


# SINGLE WORD
"""PR4: If User provides Single Word Input - Respond with basic question"""
def single_word_rule(wordlist, mapped_wordlist):
    #PR4
    if len(wordlist) == 1:
        return "Not very chatty are you.. What do you mean -  " + wordlist[0] + " ?"
    return False


# I HAVE OR I FEEL
"""PR5: If User says I have ___ : Respond with grumpy response..  You are too young """
"""PR6: If User says I feel ___ : Respond with motivational advice"""
def i_have_feel_rule_set(wordlist, mapped_wordlist):
    #PR5
    if wordlist[0:2] == ['i', 'have']:
        return "How could you say that " + stringify(mapped_wordlist[2:]) + '.' + " You are too young."

    #PR6
    if wordlist[0:2] == ['i', 'feel']:
        return "Hmmmm. Facts over feelings, love. Suck it up."

    return False


# ASKING ME A QUESTION
"""PR7: If User asks Do You ___ :  Respond with negative."""
"""PR8: If User asks Can You ___ or Could you ___: Respond with I can but I wont"""
"""PR9: If User asks Did You ___ : Respond with anecdote about previous marriage"""
"""PR10: If User asks Have you ___ : Talk about alcoholism"""
"""PR11: If User asks Will you ___  or Would you ____: Respond with an affirmative"""
def do_you_can_you_rule_set(wordlist, mapped_wordlist):
    #PR7
    if wordlist[0:2] == ['do', 'you']:
        return "No, I don't. It's been a difficult " + choice(TIME) + " for me."

    #PR8
    if wordlist[0:2] == ['can', 'you'] or wordlist[0:2] == ['could', 'you']:
        return " I can " + wordlist[0] + ' ' + stringify(mapped_wordlist[2:]) + ". But I won't."

    #PR9
    if wordlist[0:2] == ['Did', 'you']:
        return " I did " + wordlist[0] + ' ' + stringify(mapped_wordlist[2:]) + " when I was married to " + \
               +choice(PEOPLE) + "."

    #PR10
    if wordlist[0:2] == ['Have', 'you']:
        return "I have. And now I am an alcoholic who loves her " + choice(DRINKS) + "."

    #PR11
    if wordlist[0:2] == ['Will', 'you'] or wordlist[0:2] == ['Would', 'you']:
        return "Yeah. No. Sure. If you got " + choice(PEOPLE) + " to come along."
    return False



# WHO ARE YOU
"""PR12: If User asks for a name : Deflect"""
def who_are_you_rule(wordlist, mapped_wordlist):
    #PR12
    if len(wordlist) > 2 and wordlist[0:3] == ['who', 'are', 'you']:
        return "Haha! You know who."
    return False


# SIMPLE MIRROR
"""PR13: Replace You with Me, and repeat back previous statement E.g You are hungry --> I am hungry"""
def repeat_parrot_rule(wordlist, mapped_wordlist):
    #PR13
    if 'you' in mapped_wordlist or 'You' in mapped_wordlist:
        return stringify(mapped_wordlist).capitalize() + '.'
    return False


# KEYWORD BASED RULE SET
"""Following Trigger rules are tested, and one response is chosen randomly from all possible options"""
"""PR14: If User mentions because : Say I understand, offer food """
"""PR15: If User mentions like ___: Say why you don't like things anymore"""
"""PR16: If User mentions dislike or hate: Ask what user doesn't like about it"""
"""PR17: If User mentions fail : Respond with anecdote about failure"""
"""PR18: If User mentions drink : Talk about a dream about drinking"""
"""PR19: If User mentions % : Doubt the numbers and tell anecdote about someone"""
"""PR20: If User mentions dream : Short response"""
"""PR21: If User mentions love : Ask for a drink Ethel likes"""
"""PR22: If User mentions no : Talk about alcoholism / Ask user to talk"""
"""PR23: If User mentions idea : Respond with sad remark about bad ideas"""
"""PR24: If User mentions sure : Say life is a mystery"""
"""PR25: If User starts with OK/okay : Say don't be a people pleaser"""
"""PR26: If User starts with please : Say how polite"""
def keyword_rule_set(wordlist, mapped_wordlist):
    options = []
    #PR14
    if 'because' in wordlist:
        options.append(" I understand. Do you want a " + choice(FOODS) + "?")

    #PR15
    if 'like' in wordlist:
        options.append(" I wish I could like things again. I stopped because " + choice(EXCUSES) + ".")

    #PR16
    if 'dislike' in wordlist or 'hate' in wordlist:
        options.append(" What don't you like about it ? Do you even like " + choice(DRINKS) + \
                       " or is this all a lie?")
    #PR17
    if 'fail' in wordlist:
        options.append("Failure wasn't an option back then. And it isn't an option now.")

    #PR18
    if 'drink' in wordlist:
        options.append("That reminds me. I had a dream last " + choice(DAYS_OF_WEEK) + \
                       " that I had an endless supply of " + choice(COLORS) + " " + choice(DRINKS) + \
                       " and a box of  " + " as I vacationed near " + choice(PLACES))
    #PR19
    if '%' in wordlist:
        options.append("Where do you get these numbers from ? Did you know that " + choice(PEOPLE) + \
                       " was really bad at Math in school?")
    #PR20
    if 'dream' in wordlist:
        options.append("Dream on, kid")

    #PR21
    if 'love' in wordlist:
        options.append("Everything I love comes in a bottle. Can I get you some " + choice(COLORS) + " tea ?")

    #PR22
    if 'no' in wordlist:
        options.append("No? Do you know what I never say no to ? A tall glass of " + choice(COLORS) + " " + choice(DRINKS) +  " on " + choice(DAYS_OF_WEEK) +".")
        options.append("Okay then. You say something interesting instead.")

    #PR23
    if 'idea' in wordlist:
        options.append("You know what wasn't a good idea? Telling " + choice(PEOPLE) + " to lay off the " + choice(DRINKS) + ".")
        options.append("I stopped having good ideas because " + choice(EXCUSES) + ".")

    #PR24
    if 'sure' in wordlist:
        options.append("What are you so sure about? Life is a mystery that is best left unresolved.")

    #PR25
    if mapped_wordlist[0] in ['okay', 'ok']:
        options.append("Don't be a people pleaser. Now let's have some " + choice(FOODS))

    #PR26
    if mapped_wordlist[0] == 'please':
        options.append("How polite of you to say please! And I thought chivalry died.")

    # Many possible keywords triggered. Select one possible response
    if len(options) > 0:
        return choice(options)

    return False

####################################################
# CYCLIC RESPONSES - COUNT VARIABLES

cyclic_default_count = 0
cyclic_i_am_count = 0
cyclic_you_are_count = 0
cyclic_w_question_count = 0
cyclic_action_count = 0

######################################
# CYCLE BASED RULES  AND CYCLIC DEFAULT STATEMENTS

# I AM STATEMENT
"""PR27: If User says I am ___ : Choose cyclically from list"""
def i_am_rule(wordlist, mapped_wordlist):
    #PR27
    if wordlist[0:2] == ['i', 'am']:
        global cyclic_i_am_count
        I_AM_OPTIONS = ["Of course, you are " + stringify(mapped_wordlist[2:]) + '.' + "Just look at you!",
                        "Let me give you some advice. Go visit " + choice(PLACES) + " and " + choice(HOBBIES) + "."]
        cyclic_i_am_count += 1
        return I_AM_OPTIONS[cyclic_i_am_count % 2]
    return False


# W-QUESTIONS
"""PR28: If User asks W- Question : Choose response cyclically from list"""
def w_questions_rule(wordlist, mapped_wordlist):
    w = wordlist[0]
    #PR28
    if wpred(w):  # Why, Where, How, When
        global cyclic_w_question_count
        W_QUESTIONS_OPTIONS = [w.capitalize() + " indeed.. ",
                               "If I knew the answer, I would still be with " + choice(PEOPLE),
                               "Who cares ? Pass me some " + choice(DRINKS)]
        cyclic_w_question_count += 1
        return W_QUESTIONS_OPTIONS[cyclic_w_question_count % 3]
    return False


# COMMENTS ABOUT ETHEL
"""PR29: If User begins with You are ___ : Choose response cyclically from list"""
def you_are_rule(wordlist, mapped_wordlist):
    #PR29
    if wordlist[0:2] == ['you', 'are'] or wordlist[0:2] == ['are', 'you']:
        global cyclic_you_are_count
        YOU_ARE_OPTIONS = ["You bet, I am " + stringify(mapped_wordlist[2:]) + '.',
                           "Enough about me. I will only say this - " + give_super_random_opinion_and_ask(),
                           "Tell me more about yourself.",
                           "Yes. Only after I " + choice(HOBBIES) + " on " + choice(DAYS_OF_WEEK) + "."]
        cyclic_you_are_count += 1
        return YOU_ARE_OPTIONS[cyclic_you_are_count % 4]
    return False


# ACTION WORDS
"""PR30: If User starts with Action Word : Choose response cyclically from list"""
def action_word_rule(wordlist, mapped_wordlist):
    w = wordlist[0]
    #PR30
    if verbp(w):
        global cyclic_action_count
        ACTION_WORD_OPTIONS = ["I " + w + ". When I have to.",
                               "To " + w + " or not to " + w + "... I quit in 1985. So no.",
                               "Let us " + w + " when we meet... maybe the upcoming " + choice(TIME)]
        return ACTION_WORD_OPTIONS[cyclic_action_count % 3]
    return False

# DEFAULT PUNTS
"""PR31: Default Response - Choose Cyclically from list"""
def default_response():
    #PR31
    DEFAULT_RESPONSES = ['Am I thirsty or what? Want to get something to drink?',
                         'What do you think of the weird weather? Shall I get you a bottle of ' + choice(DRINKS) + \
                         " while we discuss that ?",
                         "Wow! Look how time flies!",
                         'Hey, between you and me, I could do with Netflix and a nap.',
                         "Sorry, I think I dozed off. You have a really soothing voice.",
                         'Do you know that I got caught smuggling puppies across the Canada border four times?']

    global cyclic_default_count
    cyclic_default_count += 1

    return DEFAULT_RESPONSES[cyclic_default_count % 6]

#####################################################
# RANDOM REMARKS , SUPER RANDOM REMARKS

#random
"""PR32: Response with random response"""
def random_response():
    #PR32
    RANDOM_REMARKS = ["I'm trying to recall your name.. Aaah, forget it. I shall call you Kiddo",
                      "When do you think a meteor will hit the earth?",
                      "Where am I ? Get me out of here!",
                      "I think I kept my Whiskey glasses somewhere. Let me get them"]
    return choice(RANDOM_REMARKS)

#super random
"""PR33: Respond with randomly chosen response with randomly chosen parameters"""
def give_super_random_opinion_and_ask():
    #PR33
    SUPER_RANDOM_OPINIONS = [
        "Did you know that my favorite food is " + choice(COLORS) + " " + choice(FOODS) + " which contains " + \
        choice(COLORS) + " " + choice(FOODS) + ". What do you like to eat?",
        "When I was " + str(choice(range(0, 100))) + " years old, my best friend was " + choice(
            PEOPLE) + ". Wish we met again.",
        "Can you keep a secret ? My secret stash of gold is hidden in " + choice(PLACES),
        "I like to  " + choice(HOBBIES) + " in my free time. What do you do?"]

    return choice(SUPER_RANDOM_OPINIONS)


###################################################################################################
"""
MEMORY OPERATIONS
- memory storage
- create memory
- retrieve memory
"""

# What Ethel hears from partner
MEMORY = []

#create memory
def remember_remark(mapped_wordlist):
    MEMORY.append(stringify(mapped_wordlist))

"""PR34: Respond with a stored user statement from more than 1 conversational turn ago """
#retrieves memory
def recall_remark():
    #PR34
    if len(MEMORY) < 1:
        return "You haven't said much worth remembering in the time that I've known you."

    old_remark = choice(MEMORY[:-1])
    recall_options = ["You earlier said " + old_remark + ". Let's discuss that for a second.",
                      "Do you remember telling me " + old_remark + "? Or was it the gin talking?"]

    recalled_remark = choice(recall_options)
    return recalled_remark


###################################################################################################
"""
PREPROCESSING AND HELPER FUNCTIONS
- remove punctuation
- split into words
- stringify
- map YOU-ME
- look for Action Words
- look for Question Words
- look for BYE
"""
# PREPROCESS INPUT, SEARCH FOR GOODBYE
def preprocess(the_input):
    for g in GOODBYE_WORDS:
        if match(g, the_input):
            print('See ya later! Bye.')

    wordlist = split(' ', remove_punctuation(the_input))

    # undo any initial capitalization:
    wordlist[0] = wordlist[0].lower()
    mapped_wordlist = you_me_map(wordlist)

    mapped_wordlist[0] = mapped_wordlist[0].capitalize()

    return (wordlist, mapped_wordlist)


# HELPER FUNCTIONS
def stringify(wordlist):
    'Create a string from wordlist, but with spaces between words.'
    return ' '.join(wordlist)


punctuation_pattern = compile(r"\,|\.|\?|\!|\;|\:")


def remove_punctuation(text):
    'Returns a string without any punctuation.'
    return sub(punctuation_pattern, '', text)


def wpred(w):
    'Returns True if w is one of the question words.'
    return (w in ['when', 'why', 'where', 'how', 'what'])


def dpred(w):
    'Returns True if w is an auxiliary verb.'
    return (w in ['do', 'can', 'should', 'would'])


CASE_MAP = {'i': 'you', 'I': 'you',
            'me': 'you', 'you': 'me',
            'my': 'your', 'your': 'my',
            'yours': 'mine', 'mine': 'yours',
            'am': 'are',
            'myself': 'yourself',
            'yourself': 'myself'}


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


# IDENTIFY ACTION WORDS
def verbp(w):
    'Returns True if w is one of these known verbs.'
    return (w in ['go', 'have', 'try', 'eat', 'take', 'help',
                  'make', 'get', 'jump', 'write', 'type', 'fill',
                  'put', 'turn', 'compute', 'think', 'drink', 'fix',
                  'blink', 'crash', 'crunch', 'add', 'dance', 'sing', 'exercise', 'play'])