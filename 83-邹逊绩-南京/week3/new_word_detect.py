import math
from collections import defaultdict
import re
class NewWordDetect:
    def __init__(self, corpus_path):
        self.max_word_length = 5
        self.word_count = defaultdict(int)
        self.left_neighbor = defaultdict(dict)
        self.right_neighbor = defaultdict(dict)
        self.load_corpus(corpus_path)
        self.calc_pmi()
        self.calc_entropy()
        self.calc_word_values()

    #加载语料数据，并进行统计
    def load_corpus(self, path):
        with open(path, encoding="utf8") as f:
            for line in f:
                sentence = line.strip()
                cop = re.compile("[^\u4e00-\u9fa5^a-z^A-Z^0-9]")  # 匹配不是中文、大小写、数字的其他字符
                sentence1 = cop.sub('\n', sentence).split('\n')  # 将string1中匹配到的字符替换成空字符
                for sentence2 in sentence1:
                    if len(sentence2) > 2:
                        for word_length in range(1, self.max_word_length):
                            self.ngram_count(sentence2, word_length)
        return

    #按照窗口长度取词,并记录左邻右邻
    def ngram_count(self, sentence, word_length):
        for i in range(len(sentence) - word_length + 1):
            word = sentence[i:i + word_length]
            self.word_count[word] += 1
            if i - 1 >= 0:
                char = sentence[i - 1]
                self.left_neighbor[word][char] = self.left_neighbor[word].get(char, 0) + 1
            if i + word_length < len(sentence):
                char = sentence[i +word_length]
                self.right_neighbor[word][char] = self.right_neighbor[word].get(char, 0) + 1
        return

    #计算熵
    def calc_entropy_by_word_count_dict(self, word_count_dict):
        total = sum(word_count_dict.values())
        entropy = sum([-(c / total) * math.log((c / total), 10) for c in word_count_dict.values()])
        return entropy

    #计算左右熵
    def calc_entropy(self):
        self.word_left_entropy = {}
        self.word_right_entropy = {}
        for word, count_dict in self.left_neighbor.items():
            self.word_left_entropy[word] = self.calc_entropy_by_word_count_dict(count_dict)
        for word, count_dict in self.right_neighbor.items():
            self.word_right_entropy[word] = self.calc_entropy_by_word_count_dict(count_dict)

    #统计每种词长下的词总数
    def calc_total_count_by_length(self):
        self.word_count_by_length = defaultdict(int)
        for word, count in self.word_count.items():
            self.word_count_by_length[len(word)] += count
        return

    #计算互信息(pointwise mutual information)
    def calc_pmi(self):
        self.calc_total_count_by_length()
        self.pmi = {}
        for word, count in self.word_count.items():
            p_word = count / self.word_count_by_length[len(word)]
            p_chars = 1
            for char in word:
                p_chars *= self.word_count[char] / self.word_count_by_length[1]
            self.pmi[word] = math.log(p_word / p_chars, 10) / len(word)
        return

    def calc_word_values(self):
        self.word_values = {}
        for word in self.pmi:
            if len(word) < 2:
                continue
            pmi = self.pmi.get(word, 1e-3)
            le = self.word_left_entropy.get(word, 1e-6)
            re = self.word_right_entropy.get(word, 1e-6)
            if word == "经网络":
                print("")
            self.word_values[word] = pmi * min(le,re)
        return

if __name__ == "__main__":
    nwd = NewWordDetect("sample_corpus.txt")
    # print(nwd.word_count)
    # print(nwd.left_neighbor)
    # print(nwd.right_neighbor)
    # print(nwd.pmi)
    # print(nwd.word_left_entropy)
    # print(nwd.word_right_entropy)
    value_sort = sorted([(word, count) for word, count in nwd.word_values.items()], key=lambda x:x[1], reverse=True)
    print([x for x, c in value_sort if len(x) == 2][:10])
    print([x for x, c in value_sort if len(x) == 3][:10])
    print([x for x, c in value_sort if len(x) == 4][:10])

