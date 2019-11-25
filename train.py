from mcts_alpha import Player
from game import Game
from neural_network import Policy_Network
import random
from torch import optim
import torch.nn.functional as F
import torch

device=torch.device("cuda" if torch.cuda.is_available() else "cpu")

#自我博弈 数据
datas=[]
value_network=Policy_Network(3,3).to(device)
player=Player(value_network.state_eval)
game=Game(player)


# loss  backward

batch_size=512

optimizer = optim.Adam(value_network.parameters(), lr=0.001,weight_decay=0.0005)

batch_time=1500

for batch_i in range(batch_time):

    state, visit_prob, q = game.self_play()
    datas.extend(zip(state, visit_prob, q))
    print(len(datas),"lllen")
    if(len(datas)<batch_size*1.6):

        continue


    batch=random.sample(datas,batch_size)

    datas=datas[len(datas)-int(batch_size*1.6):]

    state_list=[]
    pos_q_list=[]
    q_list=[]
    for state, visit_prob, q in batch:
        state_list.append(state)
        pos_q_list.append(visit_prob)
        q_list.append(q)

    state=torch.tensor(state_list).float().to(device)
    visit_prob=torch.stack(pos_q_list).float().to(device)
    q=torch.tensor(q_list).float().to(device)

    optimizer.zero_grad()

    output_visit_prob, output_q=value_network(state)
    print(q_list[-1])
    print(state[-1])
    print(visit_prob[-1])
    print(output_visit_prob[-1])
    print("")

    visit_prob=visit_prob.view(visit_prob.size(0),-1)
    output_visit_prob=output_visit_prob.view(output_visit_prob.size(0), -1)

    visit_prob_loss=-torch.mean(visit_prob*torch.log(output_visit_prob))

    #visit_prob_loss = F.l1_loss(visit_prob,output_visit_prob)

    q_loss=F.mse_loss(output_q,q)

    loss=visit_prob_loss+q_loss
    print(visit_prob_loss,q_loss,loss)

    loss.backward()
    optimizer.step()
