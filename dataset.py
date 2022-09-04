import torch
import json

from utils import trans

class CardData(torch.utils.data.Dataset) :
    def __init__(self, filename) :
        super(CardData, self).__init__()
        self.file = filename
        self.list = []
        with open(filename, 'r') as f:
            while True:
                s = f.readline()
                if len(s) == 0:
                    break
                self.list.append(s)
    def __len__(self):
        return len(self.list)
    def __getitem__(self, index):
        data = self.list[index]
        data = json.loads(data)
        card = data['card']
        history = data['history']
        response = data['response']

        cardmap = [[0 for i in range(15)] for x in range(4)]
        for d in card[0]:
            d = int(d)
            if d >= 52:
                cardmap[0][d-52+13] += 1
            else:
                cardmap[0][d//4] += 1
        for d in history[1]:
            d = int(d)
            if d >= 52:
                cardmap[2][d-52+13] += 1
            else:
                cardmap[2][d//4] += 1
        for d in history[2]:
            d = int(d)
            if d >= 52:
                cardmap[1][d-52+13] += 1
            else:
                cardmap[1][d//4] += 1

        for d in history[3]:
            d = int(d)
            if d >= 52:
                cardmap[3][d-52+13] += 1
            else:
                cardmap[3][d//4] += 1
        retcard = [[[0 for i in range(16)] for x in range(4)] for y in range(4)]
        for i in range(4): # 转化为one-hot
            for j in range(15):
                for k in range(cardmap[i][j]):
                    retcard[i][k][j] = 1
        for i in range(3):
            for j in range(4):
                retcard[i][j][15]=len(card[i])
        combr = trans(response, "vanilla")
        label = combr['id']
        
        retcard = torch.tensor(retcard, dtype=torch.float)
        return label, retcard