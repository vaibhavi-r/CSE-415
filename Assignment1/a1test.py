from a1 import *  #Import All Members
########################
#TEST File for Assignment 1, Part 1
########################

#Functions to Test
test_functions = ["three_x_cubed_plus_7", "mystery_code", "pair_off", "past_tense"]

#Test Case format: (input arg, expected output)
test_cases = { "three_x_cubed_plus_7" : [(2, 31),   #test1
                                         (0, 7),   #test2
                                         (1, 10),  #test3
                                         (-1111, -4113991886)  #test4
                                         ],

               "mystery_code":[("abc Iz th1s Secure? n0, no, 9!", "TUV bS MA1L lXVNKX? G0, GH, 9!"), #test5
                               ("Numb3rs :) ", "gNFU3KL :) ") , #test6
                               ("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ", "TUVWXYZABCDEFGHIJKLMNOPQRStuvwxyzabcdefghijklmnopqrs") #test7
                               ],

               "pair_off":[([2, 5, 1.5, 100, 3, 8, 7, 1, 1, 0, -2], [[2, 5], [1.5, 100], [3, 8], [7, 1], [1, 0], [-2]]), #test8
                           ([], []), #test9
                           ([1], [[1]]), #test10
                           ([1,2,3,4,5,6,7,8,9,10], [[1,2],[3,4],[5,6],[7,8],[9,10]]), #test11
                           ],

               "past_tense":[(['program', 'debug', 'execute', 'crash', 'repeat', 'eat'], ['programmed', 'debugged', 'executed', 'crashed', 'repeated', 'ate']), #test12
                             (['be', 'have', 'go'], ['was', 'had', 'went']), #test13
                             (['free', 'throw','jam', 'chime', 'roll', 'cry', 'laugh'], ['freed', 'throwed', 'jammed', 'chimed', 'rolled', 'cried', 'laughed'])] #test14
               }

#Evaluate the function with single given argument
def eval_test_function(f_name, arg):
    if f_name == 'three_x_cubed_plus_7':
        return three_x_cubed_plus_7(arg)

    elif f_name == 'mystery_code':
        return mystery_code(arg)

    elif f_name == 'pair_off':
        return pair_off(arg)

    elif f_name == 'past_tense':
        return past_tense(arg)

    else:
        return "Invalid Test Function"


#Gotta test 'em all
for f_name in test_functions:
    print("\nTesting Function :", f_name, '\n---------------------------------------')
    for (in_arg, expected_out) in test_cases[f_name]:
        print("Function Input  :" , in_arg)
        print("Expected Output :", expected_out)
        print("Actual   Output :", eval_test_function(f_name, in_arg))
        print("")

'''
### SIMPLE TESTS (DEPRECATED)
#Deprecated in favor of robust test case method written above

a1 = three_x_cubed_plus_7(2)
print(a1)

b1 = mystery_code("abc Iz th1s Secure? n0, no, 9!")
print(b1)

d1 = past_tense(['program', 'debug', 'execute', 'crash', 'repeat', 'eat'])
print(d1)

'''