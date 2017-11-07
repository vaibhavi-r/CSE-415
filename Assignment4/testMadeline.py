#import vaibhaviKInARow as player

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
        print(line.count("A"*k))