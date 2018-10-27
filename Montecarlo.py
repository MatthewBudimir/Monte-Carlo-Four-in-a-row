import random
import math
from board import Board
import time
from copy import deepcopy

class Node(object):
    """docstring for Node."""
    def __init__(self,balance,parent, game,state,player,move):
        self.moves = game.getMoves(player,state)
        self.state = state
        self.game = game
        self.player = player
        self.wins = 0
        self.visits = 0
        self.children = []
        self.balance = balance
        self.parent = parent
        self.move = move

    def simulate(self):
        if self.moves == []:
            return 0
        # If you are a new leaf node, run a playout.
        if (not self.children) and self.visits == 0:
            self.visits = 1
            result = self.playout(deepcopy(self.state))
            # if(result == self.player):
            #     self.wins = self.wins + 1
            self.wins = self.wins + result#*self.player
            return result
        # If you are a leaf node that has at least one playout, we need to spawn children.
        elif (not self.children):
            # We need to give ourselves children:
            result = 0
            for move in self.moves:
                self.children.append(Node(
                self.balance,
                self,
                self.game,
                self.game.changeState(self.player,move,deepcopy(self.state)),
                self.player*-1,
                move
                ))
            # Select a child randomly
            result = self.children[0].simulate()
            self.visits = self.visits + 1
            # if result == self.player:
            #     self.wins = self.wins + 1
            self.wins = self.wins + result#*self.player
            return result
        else:
            # Select a child that maximises UCB1: vi + C sqrt(ln(N)/ni)
            # If you are the root node:
            if self.parent is None:
                N = 1
            else:
                N = self.parent.visits
            # find the child that maximises UCB1
            maxChild = 0
            maxUCB1 = 0
            for i in range(len(self.children)):
                if self.children[i].visits == 0:
                    maxChild = i
                    break
                temp = float(self.children[i].wins)/self.children[i].visits + self.balance*math.sqrt(math.log(self.visits)/float(self.children[i].visits))
                if temp > maxUCB1:
                    # print("new max")
                    maxUCB1 = temp
                    maxChild = i

            result = self.children[maxChild].simulate()

            self.visits = self.visits +1
            # if result == self.player:
                # self.wins = self.wins +1
            self.wins = self.wins + result#*self.player
            return result

    def playout(self,state):
        # Playout a game randomly from this node.
        moves = self.game.getMoves(self.player,state)
        player = self.player
        outcome = 0
        wins = 0
        # While there are moves to make.
        while(moves):
            # randomly choose a move
            state = self.game.changeState(player,random.choice(moves),deepcopy(state))
            # find out if someone won.
            result = self.game.checkWinner(state)
            # if someone won then return that result.
            if result != 0:
                # self.game.printBoard(state)
                # print('')
                return result
            # Get the moves for the next player
            player = player*-1
            moves = self.game.getMoves(player,state)
        return 0

    def getBestMove(self):
        best = self.children[0].visits
        move = self.children[0].move
        wins = self.children[0].wins
        for child in self.children:
            if child.visits > best:
                best = child.visits
                move = child.move
                wins = child.wins
        # print('best move: ' + str(move))
        # print('best child: ' + str(best))
        # print('wins:' + str(wins))
        # print("visits:")
        # print(map(lambda x: x.visits,self.children))
        # print("UCB1:")
        # print(map(lambda child: float(child.wins)/child.visits + 2*math.sqrt(math.log(1)/child.visits),self.children))
        return move
    def printNode(self,spacing):
        print('####')
        print(spacing + "move:" + str(self.move))
        print(spacing + "wins:" + str(self.wins))
        print(spacing + "visits:" + str(self.visits))
        if spacing == '--':
            return
        for i in self.children:
            i.printNode(spacing+'-')
            

class MonteCarlo(object):
    def __init__(self,balance,game,player):
        self.balance = balance
        self.game = game
        self.player = player

    def run(self,t,state):
        root = Node(self.balance,None,self.game,state,self.player,None)
        # start = time.time()
        # now = start
        # count = 0
        # while(now-start < 5):
        for i in range(500):
            # print("simulating")
            root.simulate()
            # root.printNode('-')
            # x = raw_input("WAITING")
        # root.printNode(' ')
        return root.getBestMove()
        # Return a move

    

board = Board()
# board.printBoard()

player = -1
ai = MonteCarlo(4,board,1)

while board.getMoves(1,board.board):
    # MAKE HUMAN MOVE
    move = raw_input("MOVE:")
    if move.replace('-','',1).isdigit():
        move = int(move)
    else:
        print("Please enter a number")
        continue
    if not 0 <= move < 7:
        print("Not valid column. Try again")
        continue
    
    board.setState(board.changeState(player,move,board.board))
    state = board.board
    
    board.printBoard(board.board)
    winner = board.checkWinner(state)
    if winner == -1:
        print("winner")
        exit()
    # MAKE AI MOVE
    move = ai.run(2,board.board)
    board.setState(board.changeState(1,move,board.board))
    winner = board.checkWinner(state)
    print('')
    board.printBoard(board.board)
    if winner == 1:
        print("loser")
        exit()
    print(board.getMoves(1,board.board))
    # player = not player

# while True:
#     move = raw_input("MOVE:")
#     if move.replace('-','',1).isdigit():
#         move = int(move)
#     else:
#         print("Please enter a number")
#         continue
#     if not 0 <= move < 7:
#         print("Not valid column. Try again")
#         continue
    
#     board.setState(board.changeState(player,move,board.board))
#     state = board.board
    
#     board.printBoard()
#     if board.checkWinner(state) != 0:
#         print("winner")
#         print(1 if player else 2)
#         exit()
#     print(board.getMoves(1,board.board))
#     player = not player