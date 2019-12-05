# -*- coding: utf-8 -*
import sys
import MeCab
import math

class Mail():
    def __init__(self, label, text):
        self.label = label
        self.text = text

    def get_label(self):
        return self.label

    def get_text(self):
        return self.text

    def make_text_word_list(self):
        mecab = MeCab.Tagger("-Owakati")
        text = mecab.parse(self.text)
        word_list = text.split()
        return word_list

class Label_Word2freq():
    def __init__(self, label, word2freq):
        self.label = label
        self.word2freq = word2freq

    def get_label(self):
        return self.label

    def get_word2freq(self):
        return self.word2freq

class Label_Word2prob():
    def __init__(self, label, word2prob):
        self.label = label
        self.word2prob = word2prob

    def get_label(self):
        return self.label

    def get_word2prob(self):
        return self.word2prob

def make_label2mitigo_prob(label2word_sum):
    label2mitigo_prob = dict()
    for label in label2word_sum.keys():
        label2mitigo_prob[label] = -math.log(1 / label2word_sum[label])
    return label2mitigo_prob

def make_label2mail_count(mail_list):
    label2mail_count = dict()

    for mail in mail_list:
        label = mail.get_label()
        label2mail_count[label] = label2mail_count.get(label, 0) + 1
    return label2mail_count

def make_label2prob(mail_list):
    label2prob = dict()
    mail_count = len(mail_list)
    label2mail_count = make_label2mail_count(mail_list)
    for label in label2mail_count.keys():
        label2prob[label] = -math.log(label2mail_count[label] / mail_count)
    return label2prob

def make_label2word_freq_sum(mail_list):
    label2word_freq_sum = dict()
    for mail in mail_list:
        label = mail.get_label()
        label2word_freq_sum[label] = label2word_freq_sum.get(label, 1) + len(mail.make_text_word_list())     #未知語を最初に代入する(label2word_freq_sum.get(label, 1)の１のこと)
    return label2word_freq_sum

def make_Label_Word2freq_list(label2word_list):
    Label_Word2freq_list = []
    for label in label2word_list.keys():
        word2freq = dict()
        for word in label2word_list[label]:
            word2freq[word] = word2freq.get(word, 0) + 1
        Label_Word2freq_list.append(Label_Word2freq(label, word2freq))
    return Label_Word2freq_list

def calculate_word_prob(word_freq, word_freq_sum):
    return -math.log(float(word_freq / word_freq_sum))

def make_label_list(mail_list):
    label_list = []
    for mail in mail_list:
        for label in mail.get_label():
            if label not in label_list:
                label_list.append(label)
    return label_list

def make_label2word_list(label_list, mail_list):
    label2word_list = dict()

    for label in label_list:
        label2word_list[label] = []

    for mail in mail_list:
        label = mail.get_label()
        for word in mail.make_text_word_list():
            label2word_list[label].append(word)
    return label2word_list

def make_Label_Word2prob_list(mail_list):
    Label_Word2prob_list = []

    label_list = make_label_list(mail_list)
    label2word_list = make_label2word_list(label_list, mail_list)
    Label_Word2freq_list = make_Label_Word2freq_list(label2word_list)
    label2word_freq_sum = make_label2word_freq_sum(mail_list)

    for Label_Word2freq in Label_Word2freq_list:
        label = Label_Word2freq.get_label()
        word2freq = Label_Word2freq.get_word2freq()
        word2prob = dict()
        for word in word2freq.keys():
            word2prob[word] = calculate_word_prob(word2freq[word], label2word_freq_sum[label])
        Label_Word2prob_list.append(Label_Word2prob(label, word2prob))
    return Label_Word2prob_list, label2word_freq_sum

def make_mail_list(f):
    mail_list = []
    for line in f:
        mail_list.append(Mail(line[0], line[2:]))
    return mail_list

def read_mail_file(training_data_name):
    with open(training_data_name, "r") as f:
        mail_list = make_mail_list(f)
    return mail_list

def output_Label_Dict_list_to_file(Label_Word2prob_list, file_name):
    with open(file_name, "w") as f:
        for Label_Word2prob in Label_Word2prob_list:
            label = Label_Word2prob.get_label()
            word2prob = Label_Word2prob.get_word2prob()
            for word in word2prob.keys():
                f.write(label + " " + word + " " + str(word2prob[word]) + "\n")

def output_dict_to_file(label2prob, file_name):
    with open(file_name, "w") as f:
        for label in label2prob.keys():
            f.write(label + " " + str(label2prob[label]) + "\n")

def main():
    training_data_name = "new_training.txt"
    # training_data_name = sys.argv[1]

    mail_list = read_mail_file(training_data_name)

    Label_Word2prob_list, label2word_sum = make_Label_Word2prob_list(mail_list)
    label2mitigo_prob = make_label2mitigo_prob(label2word_sum)
    label2prob = make_label2prob(mail_list)

    output_Label_Dict_list_to_file(Label_Word2prob_list, "label_word2prob.txt")
    output_dict_to_file(label2mitigo_prob, "mitigo_prob.txt")
    output_dict_to_file(label2prob, "label2prob.txt")

if __name__ == '__main__':
    main()

