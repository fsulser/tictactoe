import random
import copy
import pprint

class TicTacToe:
    def __init__(self, player0, player1):
        self.board = [[' ' for i in range(3)] for j in range(3)]
        self.player0 = player0
        self.player1 = player1
        self.active_player = self.player0
        self.other_player = self.player1
        self.char = 'O'

    def play_game(self):
        if type(self.player0).__name__ == 'PersonPlayer' or type(self.player1).__name__ == 'PersonPlayer':
            print("\n\n New Game")
        while not(self.has_won() or self.is_finished()):
            if type(self.active_player).__name__ == 'PersonPlayer':
                self.display_board()
            row, col = self.active_player.move(self.board)
            self.board[row][col] = str(self.char)
            if self.has_won():
                self.active_player.learn(1, self.board)
                self.other_player.learn(-1, self.board)
                if type(self.player0).__name__ == 'PersonPlayer' or type(self.player1).__name__ == 'PersonPlayer':
                    self.display_board()
                    print("***********************")
            elif self.is_finished(): # tie game
                self.active_player.learn(0.5, self.board)
                self.other_player.learn(0.5, self.board)
            else:
                self.other_player.learn(0, self.board)
            self.switch_player()

    def switch_player(self):
        if self.active_player == self.player0:
            self.active_player = self.player1
            self.other_player = self.player0
            self.char = 'X'
        else:
            self.active_player = self.player0
            self.other_player = self.player1
            self.char = 'O'

    def has_won(self):
        for x in range(0,3):
            if self.board[0][x] == self.board[1][x] == self.board[2][x] != ' ':
                return True
            if self.board[x][0] == self.board[x][1] == self.board[x][2] != ' ':
                return True
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != ' ':
            return True
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != ' ':
            return True
        return False

    def is_finished(self):
        if any(' ' in sublist for sublist in self.board):
            return False
        else:
            return True

    def display_board(self):
        for x in range(0,3):
            print((' {} ¦ {} ¦ {}').format(*self.board[x]))
            if(x != 2):
                print("_____________")
#            pprint.pprint(self.board[x])


class Player(object):
    def move(self, board):
        return int(input("Your move? "))

    def learn(self, value, board):
        print("rewarded: {}".format(value))

    def available_moves(self, board):
        actions = []
        empty_rows = self.get_empty_rows(board)
        for row in range(0, len(empty_rows)):
            empty_cols = self.get_empty_cols_for_row(board, empty_rows[row])
            for col in range(0, len(empty_cols)):
                actions.append((empty_rows[row],empty_cols[col]))
        return actions

    def get_empty_rows(self, board):
        rows = []
        for x in range(0,3):
            if ' ' in board[x]:
                rows.append(x)
        return rows
        
    def get_empty_cols_for_row(self, board, row):
        cols = []
        for x in range(0,3):
            if ' ' == board[row][x]:
                cols.append(x)
        return cols

class PersonPlayer(Player):

    def move(self, board):
        text = self.get_and_validate_input(board)
        
        row = int(text[0])
        col = int(text[2])
        
        return row, col

    def get_and_validate_input(self, board):
        text = input("What's your next move? (type x and y like 0,0)")

        while (len(text)!=3 or text[1] != ',' or not self.is_integer(text[0]) or not self.is_integer(text[2])):
            text = input("Input was wrong. Try again (type x and y like 0,0)")

        x = int(text[0])
        y = int(text[2])
        if(board[x][y] != ' '):
            print("FIELD IS NOT EMPTY, CHOOSE ANOTHER ONE");
            return self.get_and_validate_input(board)

        return text

    def is_integer(seld,s):
        try: 
            int(s)
            return True
        except ValueError:
            return False
        

class QLearningPlayer(Player):
    def __init__(self, Q = {}, epsilon=0.9, alpha=0.3, gamma=0.9):
        self.breed = "Qlearner"
        self.harm_humans = False
        self.q = Q # (state, action) keys: Q values
        self.epsilon = epsilon # e-greedy chance of random exploration
        self.alpha = alpha # learning rate
        self.gamma = gamma # discount factor for future rewards
        self.last_board = [[' ' for i in range(3)] for j in range(3)]
        self.last_move = None

    def getQ(self, state, action):
        # encourage exploration; "optimistic" 1.0 initial values
        if self.q.get((str(state), action)) is None:
            self.q[(str(state), action)] = 1.0
        return self.q.get((str(state), action))

    def move(self, board):
        self.last_board = copy.deepcopy(board)
        actions = self.available_moves(board)

        if random.random() < self.epsilon:
            self.last_move = random.choice(actions)
            return self.last_move

        qs = [self.getQ(str(self.last_board), a) for a in actions]
        maxQ = max(qs)

        if qs.count(maxQ) > 1:
            # more than 1 best option; choose among them randomly
            best_options = [i for i in range(len(actions)) if qs[i] == maxQ]
            i = random.choice(best_options)
        else:
            i = qs.index(maxQ)

        self.last_move = actions[i]
        return actions[i]

    def learn(self, value, board):
        if self.last_move:
            prev = self.getQ(str(self.last_board), self.last_move)
            maxqnew = max([self.getQ(str(board), a) for a in self.available_moves(self.last_board)])
            self.q[(str(self.last_board), self.last_move)] = prev + self.alpha * ((value + self.gamma*maxqnew) - prev)


