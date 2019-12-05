import MeCab
import sys


def output_file(output_data_list):
    with open("judge_data.txt", "w") as f:
        for output_data in output_data_list:
            f.write(output_data[0] + "," + output_data[1])

def judge_max_score_label(label2score):
    label_list = []
    for key_value in label2score.items():
        if key_value[1] == min(label2score.values()):
            label_list.append(key_value[0])
    if len(label_list) == 1:
        label = label_list[0]
    else:
        label = "Error"
    return label

def calc_score(label_word_prob_list, judge_mail_words, label2score, label2mitigo_prob):
    for judge_word in judge_mail_words:
        used_label_list = []
        for label_word_prob in label_word_prob_list:
            if judge_word == label_word_prob[1]:
                label2score[label_word_prob[0]] += float(label_word_prob[2])
                used_label_list.append(label_word_prob[0])
        for label in label2score.keys():
            if label not in used_label_list:
                label2score[label] += label2mitigo_prob[label]
    return label2score

def make_label2score_base(label_prob_list):
    label2score_base = dict()
    for list in label_prob_list:
        label = list[0]
        prob = float(list[1])
        label2score_base[label] = prob
    return label2score_base

def judge_spam_mail(label_word_prob_list, label_prob_list, judge_mail_words_list, text_list, label2mitigo_prob):
    judge_and_text_list = []
    count = 0
    for judge_mail_words in judge_mail_words_list:
        judge_text = []
        label2score_base = make_label2score_base(label_prob_list)
        label2score = calc_score(label_word_prob_list, judge_mail_words, label2score_base, label2mitigo_prob)
        judge_text.append(judge_max_score_label(label2score))
        judge_text.append(text_list[count])
        judge_and_text_list.append(judge_text)
        count += 1
    return judge_and_text_list

def make_wakati_list(file_name):
    wakati_list = []
    test_list = []
    mecab = MeCab.Tagger("-Owakati")
    with open(file_name, "r") as f:
        for line in f:
            text = line[2:]
            words = mecab.parse(text)
            wakati_list.append(words.split())
            test_list.append(text)
    return wakati_list, test_list

def make_line_split_list(file_name):
    line_split_list = []
    with open(file_name, "r") as f:
        for line in f:
            line_split_list.append(line.split())
    return line_split_list

def make_dict_from_label_prob(file_name):
    label2mitigo_prob = dict()
    label_prob_list = make_line_split_list(file_name)
    for label_prob in label_prob_list:
        label = label_prob[0]
        prob = float(label_prob[1])
        label2mitigo_prob[label] = prob
    return label2mitigo_prob

def main():
    """
    label_word_prob_file_name = sys.arg[1]
    label_prob_file_name = sys.arg[2]
    judge_mail_file_name = sys.arg[3]
    mitigo_prob_file_name = sys.arg[4]
    """
    #データの入力
    label_word_prob_file_name = "label_word2prob.txt"
    label_prob_file_name = "label2prob.txt"
    judge_mail_file_name = "test_data.txt"
    mitigo_prob_file_name = "mitigo_prob.txt"

    #データの整理
    label_word_prob_list = make_line_split_list(label_word_prob_file_name)
    label_prob_list = make_line_split_list(label_prob_file_name)
    judge_mail_words_list, text_list = make_wakati_list(judge_mail_file_name)
    label2mitigo_prob = make_dict_from_label_prob(mitigo_prob_file_name)

    #メールの判定
    judge_and_text_list = judge_spam_mail(label_word_prob_list, label_prob_list, judge_mail_words_list, text_list, label2mitigo_prob)

    #結果の出力
    output_file(judge_and_text_list)

if __name__ == '__main__':
    main()