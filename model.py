import torch
import torch.nn as nn
import torch.nn.functional as nnf

class MainNet(nn.Module):
    def __init__(self) :
        super(MainNet, self).__init__()
        self.conv1 = nn.Conv2d(4, 5, 3, padding=2)
        self.conv2 = nn.Conv2d(5, 7, 2, padding=2)
        self.conv3 = nn.Conv2d(7, 9, 3, padding=2)
        self.conv4 = nn.Conv2d(9, 11, 3, padding=2)
        self.fc1 = nn.Linear(11 * 13 * 25, 1024)
        self.fc2 = nn.Linear(1024, 512)
        self.fc3 = nn.Linear(512, 448)
        self.dropout = nn.Dropout(0.5)

    def forward(self, x):
        # print(x.shape)
        #x = self.pool1(nnf.relu(self.conv1(x)))
        x = nnf.relu(self.conv1(x))
        #print(x.shape)
        x = nnf.relu(self.conv2(x))
        # print(x.shape)
        #x = self.pool2(nnf.relu(self.conv3(x)))
        x = nnf.relu(self.conv3(x))
        x = nnf.relu(self.conv4(x))
        x = x.view(-1, 11 * 13 * 25)
        x = nnf.relu(self.fc1(x))
        x = self.dropout(x)
        x = nnf.relu(self.fc2(x))
        x = self.fc3(x)
        # print(x)
        # print(x.shape)
        # x = nnf.log_softmax(x, dim=1)
        return x

# class DNet(nn.Module):
#     def __init__(self, 