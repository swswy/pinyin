import json

print('loading pre-data,please wait a moment...')

f = open('pre-data/final_pinyin2_to_word2.json', 'r', encoding='utf-8')
ps2w_dict = json.loads(f.read())
f.close()

f = open('pre-data/final_word2_to_char.json', 'r', encoding='utf-8')
ws2c_dict = json.loads(f.read())
f.close()

f = open('./pre-data/final_pinyin_to_word.json', 'r', encoding='utf-8')
p2w_dict = json.loads(f.read())
f.close()

print('loading data finished')


def hanzi(pinyin_list):
    if len(pinyin_list) == 1:
        poss = max(p2w_dict[pinyin_list[0]]['words_cnt'])
        p = p2w_dict[pinyin_list[0]]['words_cnt'].index(poss)
        ch = p2w_dict[pinyin_list[0]]['words'][p]
        return ch

    chainorder = []

    pinyin_first = pinyin_list[0] + ' ' + pinyin_list[1]
    total_first = ps2w_dict[pinyin_first]['cnt']
    char_list_pre = ps2w_dict[pinyin_first]['words']
    cnts_list_first = ps2w_dict[pinyin_first]['words_cnt']
    pre = []
    for cnt_first in cnts_list_first:
        pre.append(cnt_first / total_first)


    for n in range(2, len(pinyin_list)):
        pro = []
        order = []
        pinyin_fol = pinyin_list[n]
        pypro = pinyin_list[n - 1] + ' ' + pinyin_list[n]

        if pypro not in ps2w_dict.keys():
            char_pre = p2w_dict[pinyin_list[n - 1]]['words'][0]
            char_fol = p2w_dict[pinyin_list[n]]['words'][0]
            ps2w_dict[pypro] = {'cnt': 1, 'words': [char_pre + char_fol], 'words_cnt': [1]}
            ws2c_dict[char_pre + char_fol] = {'cnt': 1, 'char': {}}
        total_fol = ps2w_dict[pypro]['cnt']
        char_list_fol = ps2w_dict[pypro]['words']
        cnts_list_fol = ps2w_dict[pypro]['words_cnt']
        for cnt_fol in cnts_list_fol:
            pro.append(cnt_fol / total_fol)

        for i in range(len(char_list_fol)):
            maxp = 0
            p = -1
            for j in range(len(char_list_pre)):
                char_pre = char_list_pre[j]
                char_fol = char_list_fol[i][1]
                if char_pre in ws2c_dict.keys():
                    poss = 0
                    if char_fol in ws2c_dict[char_pre]['char'].keys():
                        poss = ws2c_dict[char_pre]['char'][char_fol] / ws2c_dict[char_pre]['cnt'] * pre[j]
                    else:
                        poss = 1 / ws2c_dict[char_pre]['cnt'] * pre[j]
                    if poss > maxp:
                        maxp = poss
                        p = j
            pro[i] = pro[i] * maxp
            order.append(p)

        chainorder.append(order)
        pre = pro
        char_list_pre = char_list_fol

    poss = max(pre)
    maxp = pre.index(poss)
    out_result = ''
    for i in range(2, len(pinyin_list)):
        py = pinyin_list[len(pinyin_list) - i] + ' ' + pinyin_list[len(pinyin_list) - i + 1]
        ch = ps2w_dict[py]['words'][maxp]
        out_result = ch[1] + out_result

        maxp = chainorder[len(pinyin_list) - i - 1][maxp]

    py = pinyin_list[0] + ' ' + pinyin_list[1]
    ch = ps2w_dict[py]['words'][maxp]
    out_result = ch + out_result
    return out_result


if __name__ == '__main__':

    input_str = input("please input the pinyin: ")
    while input_str:
        pinyin_list = input_str.split()
        is_wrong = False
        for pinyin in pinyin_list:
            if pinyin not in p2w_dict.keys():
                is_wrong = True
                break
        if is_wrong:
            input_str = input('please input the right pinyin: ')
        else:
            print(hanzi(pinyin_list))
            input_str = input('please input the pinyin: ')
