import sys
# import curses

class Board(object):
    """docstring for Board."""
    def __init__(self):
        super(Board, self).__init__()
        self.board = [[0]*7 for i in range(6)]
        for row in self.board:
            print row
        # print self.board
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
                            run = self.findRun(state,token,4,x,y,xShift,yShift)
                            if run:
                                return token
        return 0
    
    def findRun(self,state,token,count,x,y,xshift,yshift):
        # Find
        # Check if thing is in bounds (Faster than using 'in' with range... Maybe.)
        if 0 <= (x+xshift) < len(state) and 0 <= (y+yshift) < len(state[0]):
            if state[x+xshift][y+yshift] == token:
                if count == 1:
                    return True
                else:
                    return self.findRun(state,token,count-1,x+xshift,y+yshift,xshift,yshift)
            else:
                return False
        else:
            return False



# board = Board()
# board.printBoard()

# player = 1
# ai = MonteCarlo(2,board,-1);
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
#     player = player*-1
        

    

# import curses
# from curses import wrapper

# import time

# def main(stdscr):
#     # Make stdscr.getch non-blocking
#     stdscr.nodelay(True)
#     stdscr.clear()
#     width = 4
#     count = 0
#     direction = 1
#     while True:
#         c = stdscr.getch()
#         # Clear out anything else the user has typed in
#         curses.flushinp()
#         stdscr.clear()
#         # If the user presses p, increase the width of the springy bar
#         if c == ord('p'):
#             width += 1
#         # Draw a springy bar
#         stdscr.addstr("#" * count)
#         count += direction
#         if count == width:
#             direction = -1
#         elif count == 0:
#             direction = 1
#         # Wait 1/10 of a second. Read below to learn about how to avoid
#         # problems with using time.sleep with getch!
#         time.sleep(0.1)

"""
Calling stdscr.nodelay(True) made stdscr.getch() non-blocking. If Python gets to
that line and the user hasn't typed anything since last time, getch will return
-1, which doesn't match any key.

What if the user managed to type more than one character since the last time
getch was called? All of those characters will start to build up, and getch will
return the value for each one in the order that they came. This can cause
delayed reactions if you're writing a game. After getch, you can call
curses.flushinp to clear out the rest of the characters that the user typed.

This is a good place to talk more about getch.

Every time the user presses a key, that key's value gets stored in a list. When
getch is called, it goes to that list and pops that value. If the user manages
to press several keys before getch is called, getch will pop the least recently
added value (the oldest key pressed). The rest of the keys remain in the list!
The process continues like this. So there's a problem if there is a delay
between calls to getch: Key values can build up. If you don't want this to
happen, curses.flushinp() clears the list of inputted values. This ensures that
the next key the user presses after curses.flushinp() is what getch will return
next time it is called.
"""

"""
To continue learning about curses, checkout the addstr method to see how you can
print strings at certain y, x coordinates. You can start here:
https://docs.python.org/3/library/curses.html#window-objects
"""
# wrapper(main)
# curses.nocbreak(); stdscr.keypad(0); curses.echo()
# curses.endwin()
