import torch
from model import MainNet
from utils import trans
from utils import botzone_trans
from utils import check_valid
import copy
import json

MODEL_PATH = "./data/25.pth"
DAN_SHUN = [0, 8, 8+7, 8+7+6, 8+7+6+5, 8+7+6+5+4, 8+7+6+5+4+3, 8+7+6+5+4+3+2, 8+7+6+5+4+3+2+1]
SHUANG_SHUN = [0, 10, 10+9, 10+9+8, 10+9+8+7, 10+9+8+7+6, 10+9+8+7+6+5, 10+9+8+7+6+5+4,
    10+9+8+7+6+5+4+3, 10+9+8+7+6+5+4+3+2, 10+9+8+7+6+5+4+3+2+1]
FEIJI = [0, 11, 11+10, 11+10+9, 11+10+9+8, 11+10+9+8+7]
HANGTIAN_FEIJI = [0, 11, 11+10, 11+10+9, 11+10+9+8]

Net = MainNet()
Net.load_state_dict(torch.load(MODEL_PATH, map_location=torch.device('cpu')))



def getAns(cardmap, have_in_hand, last_out, oridata = [], if_must = False) :
    if len(have_in_hand) <= 5:
        if_must = True
    # print(last_out)
    last_out = trans(last_out, "syc")
    # print(last_out)
    cardmap = torch.tensor(cardmap, dtype=torch.float)
    cardmap = cardmap.unsqueeze(0)
    outid = Net(cardmap)
    outid = outid.squeeze(0).detach().numpy()
    id_sorted = []
    for i, data in enumerate(outid):
        id_sorted.append((-data, i))
    id_sorted = sorted(id_sorted)
    for data, i in id_sorted:
        # print(i)
        if (int(i) == 0) :# and if_must:
            continue
        ret = check_valid(have_in_hand, int(i), last_out)
        if ret['status'] == True:
            # print(i)
            # print(ret['res'])
            # continue
            # break
            ret_card = copy.deepcopy(oridata)
            res_card = copy.deepcopy(ret["res"])
            for c in oridata:
                _c = c
                if _c >= 52:
                    _c = _c - 52 + 13
                else:
                    _c = _c // 4
                if res_card.count(_c) >= 1:
                    res_card.remove(_c)
                    ret_card.remove(c)
            return ret_card
    return []

def input_trans(prompt):
    print(prompt)
    str_in = input().split(" ")
    card = []
    cardcnt = [0 for x in range(15)]
    for s in str_in:
        card.append(int(s))
        cardcnt[int(s)] += 1
    cardmap = [[0 for x in range(15)] for y in range(4)]
    for i in range(15):
        for j in range(cardcnt[i]):
            cardmap[j][i] = 1
    return card, cardmap


"""
while True:
    card = []
    cardmap = []
    _, __ = input_trans("your card:")
    card.append(_)
    cardmap.append(__)
    _, __ = input_trans("last last card:")
    card.append(_)
    cardmap.append(__)
    _, __ = input_trans("last card:")
    card.append(_)
    cardmap.append(__)

    getAns(cardmap, card[0], card[2])
"""

# 解析读入的JSON
full_input = json.loads(input())
# print(full_input)

first_req = full_input["requests"][0]
if ("bid" in first_req) and (len(full_input["requests"]) == 1):
    print(json.dumps({"response":0}))
    exit(0)

if ("bid" in first_req) :
    user_info = full_input["requests"][1]
    last_req = full_input["requests"][-1]
    my_history = full_input["responses"][1:]
else :
    user_info = full_input["requests"][0]
    last_req = full_input["requests"][-1]
    my_history = full_input["responses"][0:]

own_card_buf = user_info["own"]
own_card = []
for s in own_card_buf:
    own_card.append(int(s))

# print(user_info)

for data in my_history:
    for d in data:
        own_card.remove(int(d))
card = []
cardmap = []
_, __ = botzone_trans(own_card)
card.append(_)
cardmap.append(__)
_, __ = botzone_trans(last_req["history"][0])
card.append(_)
cardmap.append(__)
_, __ = botzone_trans(last_req["history"][1])
card.append(_)
cardmap.append(__)

# print(last_req)
# print(last_req["history"][0])
# print(last_req["history"][1])
# print(cardmap)
# print(card)

if (len(card[1]) == 0) and (len(card[2]) == 0):
    ret = getAns(cardmap, card[0], card[1], own_card, True)
elif (len(card[2]) == 0):
    ret = getAns(cardmap, card[0], card[1], own_card, False)
else:
    ret = getAns(cardmap, card[0], card[2], own_card, False)


print(json.dumps({
    "response": ret,
}))