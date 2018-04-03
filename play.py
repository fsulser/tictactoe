import ast
import os
from tictactoe import TicTacToe, QLearningPlayer, PersonPlayer

clear = lambda: os.system('cls')
clear()

with open("trained_Q.txt", "r") as text_file:
    text = str(text_file.read())
    Q = ast.literal_eval(text)
    
p2 = QLearningPlayer(Q = Q, epsilon = 0)

p1 = PersonPlayer()
p2.epsilon = 0

while True:
    t = TicTacToe(p1, p2)
    t.play_game()