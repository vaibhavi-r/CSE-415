#Function 1
def three_x_cubed_plus_7(x):
    if type(x) == int or type(x) == float:
        return (3*x*x*x)+7
    else:
        return ""


#Function 2
def mystery_code(text):
    if type(text) != str:
        return "Invalid Input!"

    ans =""
    offset = 7
    for ch in text:
        if ch.isalpha():
            if ch.isupper():
                CH = chr(97 + (ord(ch) -65 + 19)%26)
            else:
                CH = chr(65 + (ord(ch) -97 +19)%26)
        else:
            CH = ch

        ans = ans + CH
    return ans

#Function 3: PAIR OFF
def pair_off(nums):
    chunks = [nums[x:x+2] for x in range(0, len(nums),2)] #List comprehension
    return chunks


#Function 4: PAST TENSE
def past_tense(verbs):
    past_verbs = []
    irregulars = {'have':'had', 'to have':'had', 'be':'was', 'to be':'was', 'eat':'ate', 'to eat':'ate', 'go':'went', 'to go':'went'}

    vowels = ['a', 'e','i','o','u']

    for verb in verbs:
        # irregular verbs: be, have, eat, go - treat specially   `
        if verb in irregulars.keys():
            past = irregulars[verb]

        #if ends in e, add d
        elif verb.endswith("e"):
            past = verb + "d"

        #if ends with consonant then y, drop y, and add ed
        elif verb.endswith("y") and verb[-2] not in vowels:
            past = verb[:-1]+"ied"

        #if ends with 1 vowel (not 2 vowels) then consonant (not y or w), add the last consonant, and then ed
        elif verb[-3] not in vowels and verb[-2] in vowels and verb[-1] not in vowels and verb[-1] not in ['y', 'w']:
            past = verb + verb[-1]+ "ed"

        #all else, add ed
        else:
            past = verb + "ed"       #throw, weep etc will give grammatically incorrect answers

        past_verbs.append(past)
    return past_verbs





