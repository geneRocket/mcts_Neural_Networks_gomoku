from board import Board
import random
import copy
import math

class Node():
    def __init__(self,board,parent):
        self.q=0
        self.visit_count=0

        self.board=board

        self.parent=parent
        self.childs={} #(row,col) -> node


    def value(self,cput):
        return self.q/(self.visit_count+1)+cput*math.sqrt(self.parent.visit_count/(self.visit_count+1))

    def get_max_visit_action(self):
        # sort_list=sorted(self.childs.items(),key=lambda item:item[1].value(5))
        # sort_list=sort_list[:min(5,len(sort_list))]
        # ret= random.choice(sort_list)
        # return ret

        return max(self.childs.items(),key=lambda item:item[1].visit_count)[0]

    def select(self):
        # sort_list=sorted(self.childs.items(),key=lambda item:item[1].value(5))
        # sort_list=sort_list[:min(5,len(sort_list))]
        # ret= random.choice(sort_list)
        # return ret

        return max(self.childs.items(),key=lambda item:item[1].value(5))

    def is_leaf(self):
        return len(self.childs)==0



    def expand(self):
        available_pos = self.board.available_pos()
        for (x,y) in available_pos:
            new_board = copy.deepcopy(self.board)
            new_board.place_chess(x, y)

            new_node = Node(new_board, self)
            self.childs[(x,y)] = new_node

    def update_value(self,value):
        self.visit_count+=1
        self.q+=value

    def update_recursive(self,value):
        self.update_value(-value)
        if(self.parent != None):
            self.parent.update_recursive(-value)



class MCTS():
    def __init__(self,node,player):
        self.root=node
        self.player=player

        self.count_1 = 0
        self.count_2 = 0


    def simulate(self):
        node=self.root

        while not node.is_leaf():
            node=node.select()[1]
            #node.board.print_board()

            #print("")




        while True:
            is_end, win_player = node.board.is_end()
            if (is_end):
                #node.board.print_board()
                if(win_player==1):
                    self.count_1+=1
                elif(win_player==2):
                    self.count_2+=1
                print("win",self.count_1,self.count_2)
                print("")

                if (win_player == self.player):
                    node.update_recursive(1)
                else:
                    node.update_recursive(-1)
                break

            node.expand()
            available_pos=node.board.available_pos()
            pos=random.choice(available_pos)
            node=node.childs[pos]
            #node.board.print_board()
            #print("")


def get_action(board):
    node = Node(copy.deepcopy(board), None)
    mcts = MCTS(node, node.board.next_player)
    for i in range(10000):
        mcts.simulate()
    return mcts.root.get_max_visit_action()








