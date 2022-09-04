import numpy as npy
import copy

DAN_SHUN = [0, 8, 8+7, 8+7+6, 8+7+6+5, 8+7+6+5+4, 8+7+6+5+4+3, 8+7+6+5+4+3+2, 8+7+6+5+4+3+2+1]
SHUANG_SHUN = [0, 10, 10+9, 10+9+8, 10+9+8+7, 10+9+8+7+6, 10+9+8+7+6+5, 10+9+8+7+6+5+4,
    10+9+8+7+6+5+4+3, 10+9+8+7+6+5+4+3+2, 10+9+8+7+6+5+4+3+2+1]
FEIJI = [0, 11, 11+10, 11+10+9, 11+10+9+8, 11+10+9+8+7]
HANGTIAN_FEIJI = [0, 11, 11+10, 11+10+9, 11+10+9+8]

def trans(card, cardtype):
    sorted(card)
    cnt = [0 for i in range(15)]
    for c in card:
        if cardtype == "vanilla" :
            if c >= 52:
                cnt[c - 52 + 13] += 1
            else:
                cnt[c // 4] += 1
        if cardtype == "syc":
            cnt[c] += 1
    # print(cnt)
    tot = len(card)
    # 空牌
    if tot == 0:
        return {'id':0, 'combo':0, 'main':0, 'dai':[]}
    # 单牌
    if tot == 1:
        x = 0
        while cnt[x] == 0:
            x += 1
        return {'id':x, 'combo':1, 'main':x, 'dai':[]}
    
    maxId = 0 # 得到次数最多且值最小的牌
    for i in range(15):
        if cnt[i] > cnt[maxId]:
            maxId = i
    right = maxId #找到与次数最多的牌连着的最大的牌
    while (right + 1 <= 14) and (cnt[right+1] == cnt[maxId]):
        right += 1
    # print('maxId:%s[%s] right:%s'%(maxId, cnt[maxId], right))
    
    if tot == 2:
        # 对子
        if cnt[maxId] == 2:
            return {'id':16+maxId, 'combo':2, 'main':maxId, 'dai':[]}
        # 王炸
        return {'id':198, 'combo':11, 'main':13, 'dai':[]}
    # 顺子
    if cnt[maxId] == 1:
        length = right - maxId + 1
        id = 29 + DAN_SHUN[length - 5] + maxId
        return {'id':id, 'combo':3, 'main':maxId, 'dai':[]}
    # 双顺
    if cnt[maxId] == 2:
        length = right - maxId + 1
        id = 65 + SHUANG_SHUN[length - 3] + maxId
        return {'id':id, 'combo':4, 'main':maxId, 'dai':[]}
    # 三不带
    if (cnt[maxId] == 3) and (len(card) == 3) :
        return {'id':120 + maxId, 'combo':5, 'main':maxId, 'dai':[]}
    # 三带一
    if (cnt[maxId] == 3) and (len(card) == 4) :
        dai = 0
        for i in range(15):
            if (i != maxId) and (cnt[i] == 1):
                dai = i
        return {'id':133 + maxId, 'combo':6, 'main':maxId, 'dai':[dai]}
    # 三带二
    if (cnt[maxId] == 3) and (len(card) == 5) :
        dai = 0
        for i in range(15):
            if (i != maxId) and (cnt[i] == 2):
                dai = i
        return {'id':146 + maxId, 'combo':7, 'main':maxId, 'dai':[dai]}
    # 炸弹
    if (cnt[maxId] == 4) and (len(card) == 4) :
        return {'id':159 + maxId, 'combo':8, 'main':maxId, 'dai':[]}
    # 四带两张
    if (cnt[maxId] == 4) and (len(card) == 6) and (right == maxId):
        dai = []
        for i in range(15):
            if (i != maxId) and (cnt[i] == 1) :
                dai.append(i)
        return {'id':172 + maxId, 'combo':9, 'main':maxId, 'dai':dai}
    # 四带两对
    if (cnt[maxId] == 4) and (len(card) == 8) and (right == maxId):
        dai = []
        for i in range(15):
            if (i != maxId) and (cnt[i] == 2):
                dai.append(i)
        return {'id':185 + maxId, 'combo':10, 'main':maxId, 'dai':dai}
    # 飞机不带翼
    if (cnt[maxId] == 3) and ((right-maxId+1)*3 == len(card)):
        length = right - maxId + 1
        id = 199 + FEIJI[length - 2] + maxId
        return {'id':id, 'combo':12, 'main':maxId, 'dai':[]}
    # 飞机带小翼或大翼
    if cnt[maxId] == 3 :
        dai = []
        wing = 0
        length = right - maxId + 1
        for i in range(15):
            if (i >= maxId) and (i <= right) :
                continue
            if (cnt[i] >= 1):
                wing = cnt[i]
                dai.append(i)
        # 小翼
        if wing == 1:
            return {'id':244 + FEIJI[length-2] + maxId, 'combo':13, 'main':maxId, 'dai':dai}
        # 大翼
        if wing == 2:
            return {'id':289 + FEIJI[length-2] + maxId, 'combo':14, 'main':maxId, 'dai':dai}
    # 航天飞机不带翼
    if (cnt[maxId] == 4) and ((right-maxId+1)*4 == len(card)):
        length = right - maxId + 1
        id = 334 + HANGTIAN_FEIJI[length - 2] + maxId
        return {'id':id, 'combo':15, 'main':maxId, 'dai':[]}
    # 航天飞机带小翼或大翼
    if cnt[maxId] == 4:
        dai = []
        wing = 0
        length = right - maxId + 1
        for i in range(15):
            if (i >= maxId) and (i <= right) :
                continue
            if (cnt[i] >= 1):
                wing = cnt[i]
                dai.append(i)
        # 小翼
        if wing == 1:
            return {'id':372 + HANGTIAN_FEIJI[length - 2] + maxId, 'combo':16, 'main':maxId, 'dai':dai}
        # 大翼
        if wing == 2:
            return {'id':410 + HANGTIAN_FEIJI[length - 2] + maxId, 'combo':17, 'main':maxId, 'dai':dai}
    print("ERROR")

def botzone_trans(cardlist):
    card = []
    cardcnt = [0 for x in range(15)]
    for c in cardlist:
        if c >= 52:
            c = c - 52 + 13
        else:
            c = c // 4
        card.append(int(c))
        cardcnt[int(c)] += 1
    cardmap = [[0 for x in range(15)] for y in range(4)]
    for i in range(15):
        for j in range(cardcnt[i]):
            cardmap[j][i] = 1
    return card, cardmap

def check_valid(card_in_hand, out_id, last_combo):
    card_in_hand = copy.deepcopy(card_in_hand)
    list.sort(card_in_hand)
    # 过
    if out_id == 0:
        return {'status':True, 'res':card_in_hand}
    if (out_id >= 1) and (out_id <= 15):
        combo = 1
    if (out_id >= 16) and (out_id <= 28):
        combo = 2
    if (out_id >= 29) and (out_id <= 64):
        combo = 3
    if (out_id >= 65) and (out_id <= 119):
        combo = 4
    if (out_id >= 120) and (out_id <= 132):
        combo = 5
    if (out_id >= 133) and (out_id <= 145):
        combo = 6
    if (out_id >= 146) and (out_id <= 158):
        combo = 7
    if (out_id >= 159) and (out_id <= 171):
        combo = 8
    if (out_id >= 172) and (out_id <= 184):
        combo = 9
    if (out_id >= 185) and (out_id <= 197):
        combo = 10
    if out_id == 198:
        combo = 11
    if (out_id >= 199) and (out_id <= 243):
        combo = 12
    if (out_id >= 244) and (out_id <= 288):
        combo = 13
    if (out_id >= 289) and (out_id <= 333):
        combo = 14
    if (out_id >= 334) and (out_id <= 371):
        combo = 15
    if (out_id >= 372) and (out_id <= 409):
        combo = 16
    if (out_id >= 410) and (out_id <= 447):
        combo = 17
    # 王炸
    if combo == 11:
        if (card_in_hand.count(13) == 1) and (card_in_hand.count(14) == 1):
            card_in_hand.remove(13)
            card_in_hand.remove(14)
            return {'status':True, 'res':card_in_hand}
        return {'status':False}
    if last_combo["combo"] == 11: # 上家牌是王炸
        return {'status':False}
    # 炸弹
    if combo == 8:
        maincard = out_id - 159
        if (card_in_hand.count(maincard) == 4) :
            if (last_combo["combo"] != 8) or ((last_combo["combo"] == 8) and (last_combo["main"] < maincard)) :
                card_in_hand.remove(maincard)
                card_in_hand.remove(maincard)
                card_in_hand.remove(maincard)
                card_in_hand.remove(maincard)
                return {'status':True, 'res':card_in_hand}
        return {'status':False}
    if last_combo["combo"] == 8: # 上家牌是炸弹
        return {"status":False}
    if (last_combo["combo"] != 0) and (last_combo["combo"] != combo): # 剩下的牌型都不能跨牌型压牌
        return {"status":False}
    # 先判断当前选择的牌型能否出出去
    maincard = 0 #当前牌型的代表牌（最低牌）
    # 单张
    if combo == 1:
        maincard = out_id - 1
        if (card_in_hand.count(maincard) == 0):
            return {"status":False}
        card_in_hand.remove(maincard)
    # 对子
    if combo == 2:
        maincard = out_id - 16
        if (card_in_hand.count(maincard) < 2):
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
    # 单顺
    if combo == 3:
        buf = out_id - 29
        layer = 0
        while DAN_SHUN[layer+1] <= buf:
            layer = layer+1
        maincard = buf - DAN_SHUN[layer]
        length = 5 + layer
        for i in range(length):
            if (card_in_hand.count(maincard + i) == 0):
                return {"status":False}
            card_in_hand.remove(maincard + i)
    # 双顺
    if combo == 4:
        buf = out_id - 65
        layer = 0
        while SHUANG_SHUN[layer+1] <= buf:
            layer = layer + 1
        maincard = buf - SHUANG_SHUN[layer]
        length = 3 + layer
        for i in range(length):
            if (card_in_hand.count(maincard + i) < 2):
                return {"status":False}
            card_in_hand.remove(maincard + i)
            card_in_hand.remove(maincard + i)
    # 三不带
    if combo == 5:
        maincard = out_id - 120
        if (card_in_hand.count(maincard) < 3):
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
    # 三带一
    if combo == 6:
        maincard = out_id - 133
        if (card_in_hand.count(maincard) < 3):
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        flag = 0
        for c in card_in_hand:
            if c != maincard:
                flag = 1
                card_in_hand.remove(c)
                break
        if flag == 0:
            return {"status":False}
    # 三带二
    if combo == 7:
        maincard = out_id - 146
        if (card_in_hand.count(maincard) < 3):
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        flag = 0
        for i in range(15):
            if card_in_hand.count(i) >= 2:
                flag = 1
                card_in_hand.remove(i)
                card_in_hand.remove(i)
                break
        if flag == 0:
            return {"status":False}
    # 四带两张
    if combo == 9:
        maincard = out_id - 172
        if card_in_hand.count(maincard) < 4:
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        dai = 0
        for i in range(15):
            if card_in_hand.count(i) >= 1:
                dai += 1
                card_in_hand.remove(i)
                if dai == 2:
                    break
        if dai < 2:
            return {"status":False}
    # 四带两对
    if combo == 10:
        maincard = out_id - 185
        if card_in_hand.count(maincard) < 4:
            return {"status":False}
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        card_in_hand.remove(maincard)
        dai = 0
        for i in range(15):
            if card_in_hand.count(i) >= 2:
                dai += 1
                card_in_hand.remove(i)
                card_in_hand.remove(i)
                if dai == 2:
                    break
        if dai < 2:
            return {"status":False}
    # 飞机
    if (combo == 12) or (combo == 13) or (combo == 14):
        if combo == 12:
            buf = out_id - 199
        if combo == 13:
            buf = out_id - 244
        if combo == 14:
            buf = out_id - 289
        # print(buf, out_id)
        layer = 0
        while FEIJI[layer + 1] <= buf :
            layer += 1
        length = layer + 2
        maincard = buf - FEIJI[layer]
        for i in range(length):
            if card_in_hand.count(maincard + i) < 3:
                return {"status":False}
            card_in_hand.remove(maincard+i)
            card_in_hand.remove(maincard+i)
            card_in_hand.remove(maincard+i)
        if combo == 13: # 带小翼
            cnt = 0
            for i in range(15):
                if (i >= maincard) and (i <= maincard + length - 1):
                    continue
                if card_in_hand.count(i) >= 1:
                    card_in_hand.remove(i)
                    cnt = cnt + 1
                if cnt == length:
                    break
            if cnt != length:
                return {"status":False}
        if combo == 14: # 带大翼
            cnt = 0
            for i in range(15):
                if (i >= maincard) and (i <= maincard + length - 1):
                    continue
                    if card_in_hand.count(i) >= 2:
                        card_in_hand.remove(i)
                        card_in_hand.remove(i)
                        cnt += 1
                    if cnt == length:
                        break
            if cnt != length:
                return {"status":False}
    if (combo == 15) or (combo == 16) or (combo == 17): # 航天飞机
        return {"status":False}
    if last_combo['combo'] == 0:
        return {"status":True, "res":card_in_hand}
    if maincard <= last_combo['main']:
        return {"status":False}
    if (combo == 3):
        buf = last_combo["id"] - 29
        if (buf < DAN_SHUN[layer]) or (buf >= DAN_SHUN[layer + 1]):
            return {"status":False}
    if combo == 4:
        buf = last_combo["id"] - 65
        if (buf < SHUANG_SHUN[layer]) or (buf >= SHUANG_SHUN[layer+1]):
            return {"status":False}
    if combo == 12:
        buf = last_combo["id"] - 199
        if (buf < FEIJI[layer]) or (buf >= FEIJI[layer+1]):
            return {"status":False}
    if combo == 13:
        buf = last_combo["id"] - 244
        if (buf < FEIJI[layer]) or (buf >= FEIJI[layer+1]):
            return {"status":False}
    if combo == 14:
        buf = last_combo["id"] - 289
        if (buf < FEIJI[layer]) or (buf >= FEIJI[layer+1]):
            return {"status":False}
    return {"status":True, "res":card_in_hand}

'''
while True:
    str_list = input().split(' ')
    list = []
    for s in str_list:
        list.append(int(s))
    data = trans(list)
    print(list)
    print(data)
'''