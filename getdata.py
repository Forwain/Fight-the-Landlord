import json
import os
import copy
from utils import check_valid
from utils import botzone_trans
from utils import trans

DIR = './'
debug_out = open('output-6048fc6b81fb3b738e911e3b', 'w')
NB_BOT_ID = ['6048fc6b81fb3b738e911e3b'] 
dataset_size = 0

folder_list = os.listdir(DIR)
# print(folder_list)

for folder in folder_list:
    if folder[-4:] == '.zip' :
        continue
    file_list = os.listdir(DIR + '/' + folder)
    # print(file_list)
    for file in file_list:
        print('working on ' + folder + '/' + file + ' ' + str(dataset_size))
        f = open(DIR + '/' + folder + '/' + file, 'r', encoding="UTF-8")
        while True :
            buffer = f.readline()
            if len(buffer) == 0:
                break
            jsondata = json.loads(buffer)
            # debug_out.write(json.dumps(jsondata, indent=4))
            # print(json.dumps(jsondata, indent=4))
            # print(jsondata['players'])
            
            is_bot = [0, 0, 0] # 是否是 bot
            bot_id = ["", "", ""] # bot 对应ID
            for i, data in enumerate(jsondata['players']):
                is_bot[i] = (data['type'] == 'bot')
                if is_bot[i]:
                    bot_id[i] = data['bot']

            # 得到初始手牌
            card_data = json.loads(jsondata['initdata'])
            card = card_data['allocation']
            history = [[], [], []]

            for i, data in enumerate(jsondata['log']):
                if i % 2 == 0:
                    continue
                id = (i - 1) / 2 % 3
                id = int(id)
                id = str(id)
                card_used=[]
                if data[id]['verdict'] != 'OK' : # 排除异常退出的情况
                    break
                response = data[id]['response']
                data = {'card' : card, 'history' : history, 'response' : response}
                if NB_BOT_ID.count(bot_id[int(id)]) >= 1:
                    resp_card, _ = botzone_trans(response)
                    flag = 1
                    if len(resp_card) == 0:
                        flag = 0
                        # print("rep0")
                        # print(resp_card)
                        # print(card)
                        my_card, _ = botzone_trans(card[0])
                        opp_card, _ = botzone_trans(history[2])
                        if len(opp_card) == 0:
                            opp_card, _ = botzone_trans(history[1])
                        opp_card = trans(opp_card, "syc")
                        # print(my_card)
                        # print(opp_card)
                        for chs in range(1, 448):
                            if check_valid(my_card, chs, opp_card)["status"] == True:
                                flag = 1
                                break
                        '''
                        if flag == 0:
                            print("kick out!")
                        else:
                            print("write in!")
                        '''
                    if flag == 1:
                        dataset_size += 1
                        debug_out.write(json.dumps(data) + '\n')
                history[0] = response
                # print(card)
                # print(history)
                flag = 1
                for c in response:
                    # print(c)
                    if card[0].count(c) == 0: # 出牌错误
                        flag = 0
                        break
                    card[0].remove(c)
                    card_used.append(c)
                if flag == 0:
                    break
                card = [card[1], card[2], card[0],card_used]
                history = [history[1], history[2], history[0]]
            # debug_out.write('\n')