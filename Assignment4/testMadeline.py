import vaibhaviKInARow as player

#print(player.__dict__)

#print(player.nickname())

#print(player.introduce())

#player.prepare(initial_state, k, what_side_I_play, opponent_nickname)
#player.zhash()
#player.parse_initial_board()
#player.init_zobrist()
#player.update_Z_SCORE()
#player.makeMove()
#player.create_board()
#player.staticEval()
#player.flatten()
#player.utter()
#player.respond()

lines = ["****AAAA"]
for line in lines:
    for k in range(1,5):
        print("K =",k)
        #print(line.count("A"*k))

INITIAL_STATE = \
              [[[' ',' ',' '],
                [' ',' ',' '],
                [' ',' ',' ']], "X"]

STATE_1 = \
              [[['X',' ',' '],
                [' ',' ',' '],
                [' ',' ',' ']], "X"]

STATE_2 = \
              [[['O',' ',' '],
                [' ',' ',' '],
                [' ',' ',' ']], "O"]


player.prepare(INITIAL_STATE, 3, what_side_I_play ='X', opponent_nickname = 'Segundo')
#print(player.init_zobrist())
#print(player.zhash(INITIAL_STATE[0]))

#print(player.PIECE_VAL['X'])
#z0 = player.zhash(INITIAL_STATE[0])
#z1 = player.zhash(STATE_1[0])
#z2 = player.zhash(STATE_2[0])
#print(player.Z_NUM)
#print(z0)
#print(z1)
#print(z2)
#print(z1^z0)
print(player.staticEval(INITIAL_STATE))


