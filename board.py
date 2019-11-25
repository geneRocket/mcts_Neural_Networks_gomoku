import copy
import numpy as np
np.set_printoptions(precision=0)

class Board():
    def __init__(self):
        self.nrow=3
        self.ncol=3
        self.n_chess=3
        #self.board=[ [0] * self.ncol for i in range(self.nrow)]
        self.board=np.zeros((self.nrow,self.ncol))
        self.next_player=1;
        self.last_move=None

        self.available_pos_list=[]
        for i in range(self.nrow):
            for j in range(self.ncol):
                self.available_pos_list.append((i,j))


    def turn_player(self):
        if(self.next_player==1):
            self.next_player=2
        else:
            self.next_player=1

    def place_chess(self,row,col):
        if(self.board[row][col]==0):
            self.board[row][col]=self.next_player
            self.turn_player()
            self.last_move=(row,col)
            self.available_pos_list.remove((row,col))
            return True
        else:
            return False

    def is_leagl_pos(self,row,col):
        return row >= 0 and row < self.nrow and col >= 0 and col < self.ncol

    def is_end(self):
        if(self.last_move==None):
            return False,None

        row=self.last_move[0]
        col=self.last_move[1]


        #上下，左右，右上左下，左上右下
        delta=[[[-1,0],[1,0]],
               [[0, -1], [0, 1]],
               [[-1, 1], [1, -1]],
               [[-1, -1], [1, 1]],
               ]

        player=self.board[row][col]

        for i in range(4):#4个方向
            sum=1

            for j in range(2):
                new_x = row+delta[i][j][0]
                new_y = col+delta[i][j][1]
                while self.is_leagl_pos(new_x,new_y) and self.board[new_x][new_y]==player:
                    sum+=1
                    new_x += delta[i][j][0]
                    new_y += delta[i][j][1]

            if(sum>=self.n_chess):
                return True,player
        if(len(self.available_pos())==0):
            return True,None
        else:
            return False,None

    def print_board(self):
        print(" ",end=' ')
        for j in range(self.ncol):
            print(j,end=' ')
        print("")
        for i in range(self.nrow):
            print(i, end=' ')
            for j in range(self.ncol):
                if(self.board[i][j]==0):
                    print("_ ",end='')
                else:
                    print(int(self.board[i][j]),end=' ')
            print("")

    def available_pos(self):
        return self.available_pos_list

    def turn_board(self,board):
        for i in range(self.nrow):
            for j in range(self.ncol):
                if(board[i][j]==1):
                    board[i][j]=2
                elif(board[i][j]==2):
                    board[i][j]=1


    def get_same_next_player_board(self):
        ret_board=copy.deepcopy(self.board)
        if(self.next_player!=1):
            self.turn_board(ret_board)
        return ret_board

