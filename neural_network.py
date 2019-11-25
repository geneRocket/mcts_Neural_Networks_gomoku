import torch
import torch.nn as nn
import torch.nn.functional as F

class Policy_Network(nn.Module):
    def __init__(self,nrow,ncol):
        super(Policy_Network,self).__init__()

        self.nrow=nrow
        self.ncol=ncol

        self.conv1=nn.Conv2d(1,32,kernel_size=3,padding=1)
        self.conv2=nn.Conv2d(32,64,kernel_size=3,padding=1)
        self.conv3 = nn.Conv2d(64, 4, kernel_size=3, padding=1)
        self.fc1=nn.Linear(4*nrow*ncol,nrow*ncol)

        self.fc2 = nn.Linear(4 * nrow * ncol, 1)

    def forward(self,state):
        state.unsqueeze_(1)
        x=F.relu(self.conv1(state))
        x=F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))
        x=x.view(x.size(0),-1)
        visit_prob=F.softmax(self.fc1(x),dim=-1)

        q=torch.tanh(self.fc2(x))

        return visit_prob.reshape(visit_prob.size(0),self.nrow,self.ncol),q

    def state_eval(self, state):

        state=torch.tensor(state).float().unsqueeze_(0).to("cuda")
        #state = torch.tensor(state).float().unsqueeze_(0)
        visit_prob,q=self.forward(state)
        return visit_prob.squeeze_(),q.squeeze_()



# row=10
# col=10
# policy_network=Policy_Network(row,col)
# print(policy_network(torch.ones((13,1,row,col))).size())

