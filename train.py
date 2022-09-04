import torch
from torch.nn.modules.loss import MSELoss
from model import MainNet
from dataset import CardData
import os

allData = CardData("pass-6048fd3781fb3b738e9138ac")
n_val = int(len(allData) * 0.95)
n_train = len(allData) - n_val
trainData,testData=torch.utils.data.random_split(allData,[n_val,n_train])
trainLoader = torch.utils.data.DataLoader(trainData, batch_size=300, shuffle=False)
testLoader = torch.utils.data.DataLoader(testData, batch_size=300, shuffle=True)

def samecnt(a, b):
    _, pred = torch.max(b, 1)
    return (a == pred).sum()

def id2combo(id):
    combo=0
    if id == 0:
        combo = 0
    if (id >= 1) and (id <= 15):
        combo = 1
    if (id >= 16) and (id <= 28):
        combo = 2
    if (id >= 29) and (id <= 64):
        combo = 3
    if (id >= 65) and (id <= 119):
        combo = 4
    if (id >= 120) and (id <= 132):
        combo = 5
    if (id >= 133) and (id <= 145):
        combo = 6
    if (id >= 146) and (id <= 158):
        combo = 7
    if (id >= 159) and (id <= 171):
        combo = 8
    if (id >= 172) and (id <= 184):
        combo = 9
    if (id >= 185) and (id <= 197):
        combo = 10
    if id == 198:
        combo = 11
    if (id >= 199) and (id <= 243):
        combo = 12
    if (id >= 244) and (id <= 288):
        combo = 13
    if (id >= 289) and (id <= 333):
        combo = 14
    if (id >= 334) and (id <= 371):
        combo = 15
    if (id >= 372) and (id <= 409):
        combo = 16
    if (id >= 410) and (id <= 447):
        combo = 17
    return combo

def type_samecnt(a, b):
    copy_a=[]
    copy_b=[]
    for i in a:
        i=id2combo(i)
        copy_a.append(i)
    _, pred = torch.max(b, 1)
    for i in pred:
        i=id2combo(i)
        copy_b.append(i)
    copy_a=torch.tensor(copy_a)
    copy_b=torch.tensor(copy_b)
    return (copy_a == copy_b).sum()

'''
def type_trans(a, b):
    copy_a=[]
    copy_b=[]
    _, pred = torch.max(a, 1)
    for i in pred:
        i=id2combo(i)
        copy_a.append(i)
    for i in b:
        i=id2combo(i)
        copy_b.append(i)
    copy_a=torch.tensor(copy_a)
    copy_b=torch.tensor(copy_b)    
    return copy_a, copy_b 
'''

os.makedirs("./models", exist_ok=True)

net = MainNet().cuda()
criterion = torch.nn.CrossEntropyLoss() # 定义 loss 为交叉熵
opetimizer = torch.optim.SGD(net.parameters(), lr=0.01, momentum=0.9) # 设定优化器
StepLR = torch.optim.lr_scheduler.StepLR(opetimizer, step_size=10, gamma=0.65)

epoch_cnt = 185
for epoch in range(epoch_cnt):
    # for batch_id, data in enumerate(trainData):
    running_loss = 0.0
    for batch_id, (label, cardmap) in enumerate(trainLoader):
        opetimizer.zero_grad()
        cardmap = cardmap.cuda()
        label = label.cuda()
        output = net(cardmap)
        '''
        type_label, type_output=type_trans(output, label.long())
        type_label=type_label.cuda()
        type_output=type_output.cuda()
        print(type_label)
        print(type_output)
        '''
        loss = criterion(output, label.long())#+criterion(type_output, type_label.long())
        loss.backward()
        opetimizer.step()

        running_loss += loss.item()
        if batch_id % 1000 == 0 :
            print('epoch:%s batch:%s loss:%s' % (epoch, batch_id, running_loss / 1000))
            running_loss = 0
            with torch.no_grad() :
                correct_cnt = 0
                datacnt = 0
                test_cnt = 0
                type_acc_cnt=0
                for batch_id, (label, cardmap) in enumerate(testLoader):
                    label = label.cuda()
                    cardmap = cardmap.cuda()
                    output = net(cardmap)
                    correct_cnt += samecnt(label, output)
                    type_acc_cnt += type_samecnt(label,output)
                    test_cnt += len(label)
                    datacnt += 1
                    if (datacnt >= 100):
                        break
                print('acc:%s' % (correct_cnt.cpu().numpy() / test_cnt))
                print('type_acc:%s' % (type_acc_cnt.cpu().numpy() / test_cnt))
    if(epoch>180):
        torch.save(net.state_dict(), "./models/posi-48fd3781fb3b738e9138ac%s.pth" % (epoch))