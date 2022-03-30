import json
import sys
print('loading pre-data,please wait a moment...')

file = open('./pre-data/final_pinyin_to_word.json', 'r', encoding='utf-8')
p2w_dict = json.loads(file.read())
file.close()

file = open('./pre-data/final_word_to_char.json', 'r', encoding='utf-8')
w2c_dict = json.loads(file.read())
file.close()

print("loading data finished")


def hanzi(pinyin_list):
    pinyin_first = pinyin_list[0]
    total_first = p2w_dict[pinyin_first]['cnt']
    char_list_pre = p2w_dict[pinyin_first]['words']
    cnts_list_first = p2w_dict[pinyin_first]['words_cnt']
    pre = []
    for cnt_first in cnts_list_first:
        pre.append(cnt_first / total_first)

    chain_list = []

    for n in range(1, len(pinyin_list)):
        fol = []
        order = []
        pinyin_fol = pinyin_list[n]
        total_fol = p2w_dict[pinyin_fol]['cnt']
        if total_fol == 0:
            total_fol+=1
            print(pinyin_fol)
        char_list_fol = p2w_dict[pinyin_fol]['words']
        cnts_list_fol = p2w_dict[pinyin_fol]['words_cnt']
        for cnt_fol in cnts_list_fol:
            fol.append(cnt_fol / total_fol)

        for i in range(len(char_list_fol)):
            maxp = 0
            p = -1
            for j in range(len(char_list_pre)):
                char_pre = char_list_pre[j]
                char_fol = char_list_fol[i]
                if char_pre in w2c_dict.keys():
                    poss = 0
                    if char_fol in w2c_dict[char_pre]['char'].keys():
                        poss = w2c_dict[char_pre]['char'][char_fol] / w2c_dict[char_pre]['cnt'] * pre[j]
                    else:
                        poss = 1 / w2c_dict[char_pre]['cnt'] * pre[j]
                    if poss > maxp:
                        maxp = poss
                        p = j
            fol[i] = fol[i] * maxp
            order.append(p)
        chain_list.append(order)
        pre = fol
        char_list_pre = char_list_fol

    poss = max(pre)
    maxp = pre.index(poss)
    out_result = ''
    for i in range(1, len(pinyin_list)):
        pinyin = pinyin_list[len(pinyin_list) - i]
        ch = p2w_dict[pinyin]['words'][maxp]
        out_result = ch + out_result
        maxp = chain_list[len(pinyin_list) - i - 1][maxp]

    pinyin = pinyin_list[0]
    ch = p2w_dict[pinyin]['words'][maxp]
    out_result = ch + out_result
    return out_result


if __name__ == '__main__':
    input_path= './data/input.txt'
    output_path='./data/output.txt'
    if len(sys.argv)==3:
        input_path=sys.argv[1]
        output_path=sys.argv[2]

    input_file = open(input_path,'r',encoding='utf-8')
    output_file = open(output_path,'w',encoding='utf-8')
    for input_str in input_file:
        pinyin_list = input_str.split()
        is_wrong = False
        for pinyin in pinyin_list:
            if pinyin not in p2w_dict.keys():
                is_wrong=True
                print(pinyin)
                break
        if is_wrong:
            print("the file has some errors")
            break
        else:
            output_file.write(hanzi(pinyin_list)+'\n')
    input_file.close()
    output_file.close()
