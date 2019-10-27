
from abc import ABCMeta,abstractmethod
from spellcor_models import register_lang_model
from spellcor_models.nglm import NGramLanguageModel,load_language_model
from spellcor_models.nglm import train as nlgm_train


class AbstractLanguageModel:

    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_score(self, sentence,word_start_index, word_end_index):
        pass

    @abstractmethod
    def is_word(self, word):
        pass

    @abstractmethod
    def load_lang_model(self, **kwargs):
        pass

    @abstractmethod
    def word_freq(self, word):
        pass


@register_lang_model("BaseLanguageModel")
class BaseLanguageModel(AbstractLanguageModel):
    def __init__(self, model_path,**kwargs):
        super(BaseLanguageModel, self).__init__("BaseLanguageModel")
        self.language_model = None
        self.load_lang_model(model_path)

    def get_score(self, sentence, word_start_index, word_end_index):
        valid_words = sentence[word_start_index:word_end_index]
        pre_words = []
        for i in range(word_start_index-1,-1,-1):
            if sentence[i].isalpha():
                pre_words.insert(0,sentence[i])
            if len(pre_words)==2: break
        after_words = []
        for i in range(word_end_index,len(sentence)):
            if sentence[i].isalpha():
                after_words.append(sentence[i])
            if len(after_words)==2: break
        words = pre_words+valid_words+after_words
        # print(words)
        return self.language_model.score(" ".join(words))

    def is_word(self, word):
        return self.language_model.is_word(word)

    def load_lang_model(self, model_path):
        self.language_model = load_language_model(model_path)

    def word_freq(self, word):
        return self.language_model.one_gram_count_dict.get(word,0)

# if __name__ == "__main__":
#     lm = BaseLanguageModel("./tmp/nglm")
#     # print(lm.get_score(["I","am","fine","who","is","the","best","language","model"],2,3))
#     # print(lm.get_score(["I", "am", "fine"], 2, 3))
#     # print(lm.get_score(["I", "am", "fine"], 2, 3))
#     lm.get_score(["I", "am","fina"],0,1)
#     # print(registered_language_models.keys())


