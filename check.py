output_file = open("./data/output.txt",'r',encoding="utf-8")
output_content = []
total = 0
for line in output_file:
    output_content.append(line)
    total +=1
output_file.close()

answer_file = open('data/answer.txt', 'r', encoding='utf-8')
answer_content = []
for line in answer_file:
    answer_content.append(line)
answer_file.close()

result_statement = 0
result_word = 0
total_word = 0
for i in range(0,total):
    if output_content[i] == answer_content[i]:
        result_statement +=1
    total_word += len(output_content[i])
    for j in range(0,len(output_content[i])):
        if output_content[i][j] == answer_content[i][j]:
            result_word += 1
    print("{} succeed!".format(i))

print("the sentence correct rate is {}".format(result_statement/total))
print("the word correct rate is {}".format(result_word/total_word))
