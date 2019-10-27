from spellcor_models import registered_language_models
from spellcor_models import register_lang_model
from spellcor_models.languageModel import AbstractLanguageModel

register_lang_model = register_lang_model
AbstractLanguageModel = AbstractLanguageModel

import spellcor_utils

class SpellChecker:
    def __init__(self):
        self.language_model = None
        self.language_model_name = None
        self.valid_word_dict = None
        self.use_valid_word_dict = False
        self.valid_candidate_dict = None
        self.use_valid_candidate_dict = False
        self._known_penalty = 20.0
        self._unknown_penalty = 4.0
        self.alphas = "qwertyuiopasdfghjklzxcvbnm"
        self.MaxCandidatesToCheck = 14

    @property
    def known_penalty(self): return self._known_penalty
    @known_penalty.setter
    def known_penalty(self, value): self._known_penalty = value
    @property
    def unknown_penalty(self): return self._unknown_penalty
    @unknown_penalty.setter
    def unknown_penalty(self, value): self._unknown_penalty = value

    def load_valid_word_dict(self,dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = [l.strip().lower() for l in lines]
        if lines: self.use_valid_word_dict = True
        self.valid_word_dict = set(lines)

    def load_valid_candidate_dict(self, dict_path):
        with open(dict_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        lines = [l.strip().lower() for l in lines]
        if lines: self.use_valid_candidate_dict = True
        self.valid_candidate_dict = set(lines)

    def load_lang_model(self,model_name,model_path,**kwargs):
        print("Loading...")
        if model_name not in registered_language_models:
            raise Exception("Language model name is not correct, call show_lang_model function to list all available "
                            "models!")
        self.language_model_name = model_name
        self.language_model = registered_language_models[model_name](model_path, **kwargs)
        print("Load Success!")

    @staticmethod
    def show_lang_models():
        models_name = list(registered_language_models.keys())
        print(models_name)
        return models_name

    def fix_sentence(self, sentence):
        tokens,lower_tokens = spellcor_utils.token_string(sentence)
        fixed_tokens = []
        # print(lower_tokens)
        for i, t in enumerate(lower_tokens):
            candidates = self.fix_pos(lower_tokens, i)
            # print(candidates)
            fixed_tokens.append(candidates[0])
        fixed_tokens = self.__align_capital(tokens, fixed_tokens)
        return "".join(fixed_tokens)

    @staticmethod
    def __align_capital(orig_tokens, fixed_tokens):
        capital_tokens = []
        for st, tt in zip(orig_tokens,fixed_tokens):
            if st == tt:
                capital_tokens.append(tt)
            else:
                capital_tokens.append(spellcor_utils.align_capital(st, tt))
        return capital_tokens

    def fix_pos(self, tokens, i):
        if i>len(tokens) or i<0: return []
        word = tokens[i]
        if not word.isalpha(): return [word]
        candidates, is_further = self.__generate_candidates(word)
        if not candidates : return [word]
        penalty_fun = self.get_penalty_func(word, is_further)
        candidates = self.__sort_candidate(candidates, tokens, i, penalty_fun)
        return candidates

    def get_penalty_func(self, word, is_further):
        def func(candidate, score):
            if word == candidate:
                return score
            elif self.__is_word(word):
                if is_further:
                    return score*2
                else:
                    return score - self.known_penalty
            else:
                return score-self.unknown_penalty
        return func

    def __is_word(self, word):
        if self.use_valid_word_dict:
            return word in self.valid_word_dict
        else:
            return self.language_model.is_word(word)

    def __valid_candidate(self,word):
        if self.use_valid_candidate_dict:
            return word in self.valid_candidate_dict
        else:
            return self.language_model.is_word(word)

    def __generate_candidates(self, word):
        """language model dict and edit distance generate candidates"""
        further_candidates = False
        candidates = spellcor_utils.edit_distance_1(self.alphas, word, self.__valid_candidate, last_level=True)
        candidates = [c for c in candidates if self.__valid_candidate(c)]
        if not candidates :
            candidates = spellcor_utils.edit_distance_2(self.alphas, word, self.__valid_candidate)
            candidates = [c for c in candidates if self.__valid_candidate(c)]
            further_candidates = True
        if candidates:
            candidates = self.filter_candidates(candidates)
            candidates.append(word)
        return list(set(candidates)), further_candidates

    def filter_candidates(self,candidates):
        if len(candidates) < self.MaxCandidatesToCheck:
            return candidates
        else:

            candidates = sorted(candidates, key = lambda x: self.language_model.word_freq(x), reverse= True)
            return candidates[:self.MaxCandidatesToCheck]

    def __sort_candidate(self,candidates, tokens, pos, penalty_func):
        """sort candidates based on language model score"""
        candidates_score_pair = []
        for c in candidates:
            cand_tokens = tokens[:]
            cand_tokens[pos] = c
            score = self.language_model.get_score(cand_tokens, pos, pos+1)
            score = penalty_func(c, score)
            candidates_score_pair.append([c, score])
        candidates_score_pair = sorted(candidates_score_pair, key=lambda x: x[1], reverse=True)
        candidates = [c for c, s in candidates_score_pair]
        return candidates


if __name__ == "__main__":
    import sys
    action = sys.argv[1]
    from spellcor_models import nglm
    if action == "train":
        assert len(sys.argv) == 4
        data_path = sys.argv[2]
        model_path = sys.argv[3]
        print("training language model....")
        print("reading data from :"+data_path)
        nglm.train(data_path, model_path)
        print("output language model to :"+model_path)




