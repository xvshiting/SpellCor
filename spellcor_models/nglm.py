"""
my 3-gram language model
"""
import codecs
import os
import pickle
import  spellcor_utils
import re
from collections import Counter
import math

model_name = "nglm.bin"
UNK = "$unk$"


class NGramLanguageModel:
    def __init__(self):
        self.one_gram_count_dict = dict()
        self.two_gram_count_dict = dict()
        self.tri_gram_count_dict = dict()
        self.K = 0.05
        self.total_words = 0
        self.vocab_size = 0
        self.UNK = UNK
        pass

    def get_gram_1_prob(self, word):
        counts_gram_1 = self.one_gram_count_dict.get(word, 0)
        counts_gram_1 += self.K
        return float(counts_gram_1) / (self.total_words + self.vocab_size)

    def get_gram_2_prob(self, word1, word2):
        counts_gram_1 = self.one_gram_count_dict.get(word1, 0)
        counts_gram_2 = self.two_gram_count_dict.get((word1, word2), 0)
        if counts_gram_2 > counts_gram_1: counts_gram_2 = 0
        counts_gram_1 += self.total_words
        counts_gram_2 += self.K
        return float(counts_gram_2) / counts_gram_1

    def get_gram_3_prob(self, word1, word2, word3):
        counts_gram_2 = self.two_gram_count_dict.get((word1, word2), 0)
        counts_gram_3 = self.tri_gram_count_dict.get((word1, word2, word3), 0)
        if counts_gram_3 > counts_gram_2: counts_gram_3 = 0
        counts_gram_2 += self.total_words
        counts_gram_3 += self.K
        return float(counts_gram_3) / counts_gram_2

    def score(self, sentence):
        # print(" score sentences:"+sentence)
        sentence = self.clean_sentence(sentence)
        sentence = sentence.split()
        if not sentence:
            return -float("Inf")
        # window_size = 3
        log_sum = 0
        # weights = [0.00001, 0.001, 1]
        sentence.extend([self.UNK, self.UNK])
        for i in range(len(sentence)-2):
            log_sum += math.log(self.get_gram_1_prob(sentence[i]))
            log_sum += math.log(self.get_gram_2_prob(sentence[i], sentence[i+1]))
            log_sum += math.log(self.get_gram_3_prob(sentence[i], sentence[i+1], sentence[i+2]))
        # print("score:",log_sum)
        return log_sum

    def is_word(self, word):
        return word.lower() in self.one_gram_count_dict

    @staticmethod
    def clean_sentence(sen):
        sen = sen.strip().lower()
        # only keep alphas delete other symbols
        sen = re.sub(r"\W", " ", sen)
        sen = re.sub(r"\d", " ", sen)
        sen = re.sub(r"\s+", " ", sen)
        return sen


def extract_n_gram(sentence):
    sentence = sentence.strip()
    sentence = sentence.split()
    one_gram, two_gram, tri_gram = sentence, [], []
    for i in range(len(sentence)):
        two_gram_end = i+1
        tri_gram_end = i+2
        if two_gram_end < len(sentence): two_gram.append(tuple(sentence[i:two_gram_end+1]))
        if tri_gram_end < len(sentence): tri_gram.append(tuple(sentence[i:tri_gram_end+1]))
    return one_gram, two_gram, tri_gram


def filter_gram_by_count(gram_dict, threshold=10):
    """
    smooth compute prob
    """
    prob_dict = dict()
    total_num = sum(gram_dict.values())
    lam = len(gram_dict)
    gram_dict = {k: v for k, v in gram_dict.items() if v > threshold}
    # for k, v in gram_dict.items():
    #     prob_dict[k] = (float(v)+1)/(total_num+lam)
    # # add prob for unk
    # prob_dict[UNK] = float(1)/(total_num+lam)
    # return prob_dict
    return gram_dict


def train_with_text(sentences):
    language_model = NGramLanguageModel()
    one_gram_dict = Counter()
    two_gram_dict = Counter()
    tri_gram_dict = Counter()
    for s in sentences:
        one_gram, two_gram, tri_gram = extract_n_gram(s)
        one_gram_dict.update(one_gram)
        two_gram_dict.update(two_gram)
        tri_gram_dict.update(tri_gram)
    language_model.one_gram_count_dict = filter_gram_by_count(one_gram_dict)
    language_model.two_gram_count_dict = filter_gram_by_count(two_gram_dict)
    language_model.tri_gram_count_dict = filter_gram_by_count(tri_gram_dict)
    language_model.total_words = sum(language_model.one_gram_count_dict.values())
    language_model.vocab_size = len(language_model.one_gram_count_dict)
    return language_model


def train(file_path, save_path = os.path.join("~", "tmp")):
    spellcor_utils.maybe_mkdir(save_path)
    language_model_file = os.path.join(save_path,model_name)
    with codecs.open(file_path, 'r', encoding="utf-8") as f:
        sentences = f.readlines()
    # clean sentence
    sentences = [ NGramLanguageModel.clean_sentence(s) for s in sentences]
    language_model = train_with_text(sentences)
    save_model(language_model, language_model_file)
    return language_model


def save_model(model,save_path):
    model_params = {"one_gram_count_dict": model.one_gram_count_dict,
                    "two_gram_count_dict": model.two_gram_count_dict,
                    "tri_gram_count_dict": model.tri_gram_count_dict,
                    "total_words": model.total_words,
                    "vocab_size": model.vocab_size
                    }
    with open(save_path, 'wb') as f:
        pickle.dump(model_params, f)


def load_language_model(model_path):
    with open(model_path, 'rb') as f:
        model_params = pickle.load(f)
    lm = NGramLanguageModel()
    for k,v in model_params.items():
        if k in lm.__dict__:
            lm.__dict__[k] = v
    return lm


if __name__ == "__main__":
    # lm = train("./data/wiki_news_600k.txt","./tmp")
    lm = load_language_model("./tmp/nglm.bin")
    print(lm.score("hello you"))
    print(lm.score("I dog okay"))
    print(lm.score("they are country for us"))
    print(lm.score("I am a student"))
    print(lm.score("I am fine"))
    print(lm.score("I am wjk"))
    print(lm.score("hfkjhkfa"))
    print(lm.score("hello"))
    print(lm.score("fina"))
    print(lm.one_gram_count_dict["fine"])
    print(lm.one_gram_count_dict["find"])
    print(lm.two_gram_count_dict.get(("am","fine"),0))
    print(lm.two_gram_count_dict.get(("am", "find"),0))


    # save_model(lm,"./tmp/nglm.bin")



