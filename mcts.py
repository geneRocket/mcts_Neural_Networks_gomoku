from board import Board
import random
import copy
import math

class Node():
    def __init__(self,parent):
        self.q=0
        self.q_sum=0
        self.visit_count=0


        self.parent=parent
        self.childs={} #(row,col) -> node


    def value(self,cput=5):
        if(self.visit_count==0):
            return  cput * math.sqrt(self.parent.visit_count)/0.0001
        return self.q + cput*math.sqrt(self.parent.visit_count)/(self.visit_count)

    def get_max_q_action(self):
        node=max(self.childs.items(), key=lambda item: item[1].q)[1]
        print(node.q,node.visit_count,(node.q+1)/2)
        return max(self.childs.items(),key=lambda item:item[1].q)[0]

        # node = max(self.childs.items(), key=lambda item: item[1].visit_count)[1]
        # print(node.q, node.visit_count, (node.q + 1) / 2)
        # return max(self.childs.items(), key=lambda item: item[1].visit_count)[0]

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



    def expand(self,available_pos):
        for (x,y) in available_pos:
            new_node = Node(self)
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
    def __init__(self,node):
        self.root=node

        self.count_1 = 0
        self.count_2 = 0


    def simulate(self,board):
        node=self.root


        while not node.is_leaf():
            pos,node=node.select()

            board.place_chess(pos[0],pos[1])
            #node.board.print_board()

            #print("")




        while True:
            is_end, win_player = board.is_end()
            if (is_end):
                #node.board.print_board()
                if(win_player==1):
                    self.count_1+=1
                elif(win_player==2):
                    self.count_2+=1
                print("win",self.count_1,self.count_2)

                if (win_player != None):
                    node.update_recursive(1)
                break

            available_pos = board.available_pos()
            node.expand(available_pos)
            pos=random.choice(available_pos)
            node=node.childs[pos]
            board.place_chess(pos[0], pos[1])
            #node.board.print_board()
            #print("")


def get_action(board):
    node = Node(None)
    mcts = MCTS(node)
    for i in range(3000):
        mcts.simulate(copy.deepcopy(board))
    print([mcts.root.childs[key].visit_count  for key in mcts.root.childs])
    print([(mcts.root.childs[key].q+1)/2 for key in mcts.root.childs])
    return mcts.root.get_max_q_action()








