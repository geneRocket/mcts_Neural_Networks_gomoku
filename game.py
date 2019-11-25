from board import Board
import gc
import numpy as np

class Game():
    def __init__(self,player):

        self.player=player


    def human_play(self):
        self.board = Board()
        while(True):
            pos=self.player.get_action(self.board)
            gc.collect()
            self.board.place_chess(pos[0],pos[1])
            print(pos[0],pos[1])
            self.board.print_board()
            if (self.board.is_end()[0]):
                break
            while True:
                str = input("x,y：")
                x=int(str.split(',')[0])
                y = int(str.split(',')[1])
                if self.board.place_chess(x,y):
                    break

            self.board.print_board()
            if(self.board.is_end()[0]):
                break



    def self_play(self):
        self.board = Board()
        states=[]
        visit_prob_list=[]

        while (True):

            pos,visit_prob = self.player.get_action(self.board)

            gc.collect()
            states.append(self.board.get_same_next_player_board())
            visit_prob_list.append(visit_prob)
            self.board.place_chess(pos[0], pos[1])


            is_end,winner=self.board.is_end()
            if (is_end):
                is_win=np.zeros(len(states))
                if(winner!=None):
                    is_win[::-2] = 1

                return states,visit_prob_list,is_win



