from board import Board
from mcts import get_action
import gc

class Game():
    def __init__(self):
        self.board = Board()



    def play(self):
        while(True):
            pos=get_action(self.board)
            gc.collect()
            self.board.place_chess(pos[0],pos[1])
            print(pos[0],pos[1])
            self.board.print_board()
            if (self.board.is_end()[0]):
                break
            str = input("x,y：")
            x=int(str.split(',')[0])
            y = int(str.split(',')[1])
            self.board.place_chess(x,y)
            self.board.print_board()
            if(self.board.is_end()[0]):
                break


game=Game()
game.play()
