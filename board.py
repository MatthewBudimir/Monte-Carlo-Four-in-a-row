import sys
from copy import deepcopy
# import curses

class Board(object):
    """docstring for Board."""
    def __init__(self):
        super(Board, self).__init__()
        self.board = [[0]*7 for i in range(6)]
    def changeState(self,player,move,state):
        # If this col is not full
        if state[0][move] == 0:
            # Go down until it's not empty
            for i in range(6):
                if state[i][move] != 0:
                    # print('ding')
                    state[i-1][move] = player
                    # Don't do anything else.
                    return state
            # if we got here then the bottom value should be filled.
            state[5][move] = player
        return state

    def getMoves(self,player,state):
        moves = [];
        for i in range(7):
            if state[0][i] == 0:
                moves.append(i)
        return moves
    def setState(self,state):
        self.board = state
    def printBoard(self,state):
        tokens = {0:'_',-1:'$',1:'#'}
        for row in state:
            for cell in row:
                token = tokens[cell]
                sys.stdout.write(str(token) + ' ')
            sys.stdout.write('\n')
        print("0 1 2 3 4 5 6")
        
    def checkWinner(self,state):
        # go through the boardstate:
        for token in [-1,1]:
            for x in range(len(state)):
                for y in range(len(state[x])):
                    # From this position: search the space in all 8 directions
                    for xShift in [1,0,-1]:
                        for yShift in [1,0,-1]:
                            if xShift == 0 and yShift == 0:
                                continue
                            # print("Start")
                            run = False
                            if state[x][y] == token:
                                run = self.findRun(state,token,4,x,y,xShift,yShift)
                            if run:
                                return token
        return 0
    
    def findRun(self,state,token,count,x,y,xshift,yshift):
        # Find
        # Check if thing is in bounds (Faster than using 'in' with range... Maybe.)
        if 0 <= (x+xshift) < len(state) and 0 <= (y+yshift) < len(state[0]):
            if state[x+xshift][y+yshift] == token:
                if count == 2:
                    return True

                else:
                    return self.findRun(state,token,count-1,x+xshift,y+yshift,xshift,yshift)
            else:
                return False
        else:
            return False
