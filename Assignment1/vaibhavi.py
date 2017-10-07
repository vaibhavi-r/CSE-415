"""
CSE 415 - Autumn 2017
Assignment 1 Part 2
Creating a generic cool grandma chatbot.

Author - Vaibhavi Rangarajan
"""
############################################################
""" LIBRARIES AND GLOBAL STATE VARIABLES
"""
# LIBRARIES
from vaibhavi_knowledge import *

############################################################
# GLOBAL STATE VARIABLES
#partner_name = "Kiddo"  # Someday, I will learn the partner's name by parsing the chat
total_responses = 0

have_greeted = False
have_mirrored = False
have_defaulted = False
have_random_responded = False
have_super_random_responded = False
have_displayed_memory = False
have_responded_single_word = False

############################################################
"""MAIN AGENT FUNCTIONS
- introduce()
- agentName()
- Ethel() --> Main Function
- respond() --> Controlling Function for Rule Base
"""

def agentName():
    return "Ethel"

def introduce():
    return ("Hi! I am Ethel and welcome to " + choice(PLACES) + "." +\
            "\n I've lived an interesting life for 120 years - and I like to gossip and celebrate it !" +\
            "\nAnd before I forget, call my caretaker, Vaibhavi Rangarajan at vaibhavi@uw.edu, if you need anything.")

def Ethel():
    'Ethel is the top-level function, containing the main loop.'
    introduce()
    while True:
        the_input = input('TYPE HERE:>> ')
        print(respond(the_input))  # Controls the entire response

###############################################################

# CONTROLLING LOGIC
# The brain of the response.
# Goes through rules, and rule sets and returns response
#Production Rules are explained in the file vaibhavi_knowledge.py

def respond(the_input):
    global total_responses

    global have_greeted
    global have_mirrored
    global have_defaulted
    global have_random_responded
    global have_super_random_responded
    global have_displayed_memory
    global have_responded_single_word

    total_responses += 1

    # FIND WORD LIST and MAPPED WORDLIST
    wordlist, mapped_wordlist = preprocess(the_input)

    #EMPTY INPUT
    res = empty_wordlist_rule(wordlist, mapped_wordlist)
    if res != False:
        return res

    #GREETING
    if have_greeted == False and total_responses <= 2:
        res = check_for_greeting_rule_set(wordlist, mapped_wordlist)
        if res!= False:
            have_greeted = True
            return res

    #REMEMBER FOR FUTURE USE (Greeting is not worth remembering)
    remember_remark(mapped_wordlist)

    #CHECK FOR W-QUESTIONS
    res = w_questions_rule(wordlist, mapped_wordlist)
    if res!=False:
        return res

    #CHECK FOR ACTION
    res = action_word_rule(wordlist, mapped_wordlist)
    if res!=False:
        return res

    #SET OF KEYWORD MATCHES
    res = keyword_rule_set(wordlist, mapped_wordlist)
    if res!=False:
        return res

    #RESPOND TO YOU ARE___
    res = you_are_rule(wordlist, mapped_wordlist)
    if res != False:
        return res

    #RESPOND TO I AM ___
    res = i_am_rule(wordlist, mapped_wordlist)
    if res != False:
        return res

    #WHO ARE YOU
    res = who_are_you_rule(wordlist, mapped_wordlist)
    if res != False:
        return res

    #SINGLE WORD
    if have_responded_single_word == False:
        res = single_word_rule(wordlist, mapped_wordlist)
        if res != False:
            have_responded_single_word = True
            return res

    #SET OF QUESTIONS - DO YOU / CAN YOU
    res = do_you_can_you_rule_set(wordlist, mapped_wordlist)
    if res!= False:
        return res

    #SHOW OFF MEMORY
    if have_displayed_memory == False and total_responses > 5:
        res = recall_remark()
        if res != False:
            have_displayed_memory = True
            return res

    #I HAVE/ I FEEL
    res = i_have_feel_rule_set(wordlist, mapped_wordlist)
    if res!= False:
        return res

    # REPEAT LIKE TODDLER PARROT RULE
    if have_mirrored == False and total_responses > 6:
        res = repeat_parrot_rule(wordlist, mapped_wordlist)
        if res!= False:
            have_mirrored = True
            return res

    # RANDOM RESPONSE
    if have_random_responded == False and have_defaulted == True:
        have_random_responded = True
        return random_response()

    # SUPER RANDOM RESPONSE
    if have_super_random_responded == False and total_responses < 3:
        have_super_random_responded = True
        return give_super_random_opinion_and_ask()

    # DEFAULT RESPONSE
    have_defaulted = True
    return default_response()

##########################################################################
# LAUNCH PROGRAM
if __name__ == "__main__":
    Ethel()
##########################################################################