from tictactoe import TicTacToe, QLearningPlayer

p1 = QLearningPlayer()
p2 = QLearningPlayer()

for i in range(0,200000):
    t = TicTacToe(p1, p2)
    t.play_game()

with open("trained_Q.txt", "w") as text_file:
    text_file.write(str(p2.q))
