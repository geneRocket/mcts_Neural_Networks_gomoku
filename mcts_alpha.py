from board import Board
import random
import copy
import math

class Node():
    def __init__(self,parent,q):
        self.q=0
        self.q_sum=0
        self.visit_count=0
        self.explorate_factor=q


        self.parent=parent
        self.childs={} #(row,col) -> node


    def value(self,cput=5):
        if(self.visit_count==0):
            return  cput *self.explorate_factor* math.sqrt(self.parent.visit_count)/0.0001
        return self.q + cput*self.explorate_factor*math.sqrt(self.parent.visit_count)/(self.visit_count)

    def get_available_pos_visit(self):

        # available pos, visit

        available_pos_visit=[(item[0],item[1].visit_count) for item in self.childs.items()]
        available_pos=[pos for (pos,visit_count) in available_pos_visit]
        visit_count=[visit_count for (pos,visit_count) in available_pos_visit]


        return available_pos,visit_count



    def select(self):
        items_list=sorted(self.childs.items(),key=lambda item:item[1].value(),reverse=True)

        max_list=[]
        for item in items_list:
            if(item[1].value()==items_list[0][1].value()):
                max_list.append(item)

        ret=random.choice(max_list)
        return ret

    def is_leaf(self):
        return len(self.childs)==0



    def expand(self,available_pos,pos_q):
        for (x,y) in available_pos:
            new_node = Node(self,pos_q[x][y])
            self.childs[(x,y)] = new_node

    def update_value(self,value):
        self.visit_count+=1
        self.q_sum+=value
        self.q=self.q_sum/self.visit_count

    def update_recursive(self,value):
        self.update_value(value)
        if(self.parent != None):
            self.parent.update_recursive(-value)



class MCTS():
    def __init__(self,node,pos_evaluate):
        self.root=node
        self.pos_evaluate=pos_evaluate




    def simulate(self,board):
        node=self.root


        while not node.is_leaf():
            pos,node=node.select()
            board.place_chess(pos[0],pos[1])
            #node.board.print_board()

            #print("")



        is_end, win_player = board.is_end()
        if (is_end):
            # node.board.print_board()
            if (win_player != None):
                leave_value=1
            else:
                leave_value=0
        else:
            visit_prob, leave_value = self.pos_evaluate(board.get_same_next_player_board())
            available_pos = board.available_pos()
            node.expand(available_pos,visit_prob)
        node.update_recursive(leave_value)


import torch
import numpy as np

class Player():
    def __init__(self, state_eval):
        self.state_eval=state_eval


    def get_action(self,board):
        node = Node(None, 1)
        mcts = MCTS(node, self.state_eval)
        for i in range(100):
            mcts.simulate(copy.deepcopy(board))


        available_pos,visit_count=mcts.root.get_available_pos_visit()

        visit_count=torch.tensor(visit_count).float()


        #visit_prob = torch.exp(visit_count)  / (torch.sum(torch.exp(visit_count)))  # softmax

        visit_prob = visit_count / torch.sum(visit_count)



        pos_index=np.random.choice(len(available_pos),p=visit_prob.numpy())
        pos=available_pos[pos_index]

        visit_prob_2_dim=torch.zeros((board.nrow,board.ncol)).float()

        for i in range(len(available_pos)):
            x,y=available_pos[i]
            visit_prob_2_dim[x][y]=visit_prob[i]



        return pos,visit_prob_2_dim








