import sys

def count_correct_answer_and_calc(correct_answer, numerator_list, denominator_list):
    deno = 0
    nume = 0
    for i in range(len(numerator_list)):
        if denominator_list[i][0] == correct_answer:
            deno += 1
            if numerator_list[i][0] == correct_answer:
                nume += 1
    return nume / deno

def calc_Precision(correct_answer, test_label_text_list, judge_label_text_list):
    return count_correct_answer_and_calc(correct_answer, test_label_text_list, judge_label_text_list)

def calc_Recall(correct_answer, test_label_text_list, judge_label_text_list):
    return count_correct_answer_and_calc(correct_answer, judge_label_text_list, test_label_text_list)

def make_label_text(file_name):
    label_text_list = []
    with open(file_name, "r") as f:
        for line in f:
            label_text_list.append(line.split(',', 1))
    return label_text_list

def main():
    #必要なデータの読み込み
    test_data_name = sys.argv[1]
    judge_data_name = sys.argv[2]
    correct_answer = sys.argv[3]
    '''
    test_data_name = "test_data.txt"
    judge_data_name = "judge_data.txt"
    correct_answer = "S"
    '''

    #データの整理
    test_label_text_list = make_label_text(test_data_name)
    judge_label_text_list = make_label_text(judge_data_name)

    #結果の表示
    print(correct_answer + "の判定")
    print("適合率：" + str(calc_Precision(correct_answer, test_label_text_list, judge_label_text_list)))
    print("再現率：" + str(calc_Recall(correct_answer, test_label_text_list, judge_label_text_list)))

if __name__ == '__main__':
    main()