import torch
import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.fc1 = nn.Linear(5, 50)
        self.fc2 = nn.Linear(50,100)
        self.fc3 = nn.Linear(100,60)
        self.fc4 = nn.Linear(60,20)
        self.fc5 = nn.Linear(20,2)

    def forward(self, x):
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc1(x))
        x = self.fc3(x)
        return x
net = Net()

input = torch.randn(5)
print(input)
out = net(input)
print(out)
