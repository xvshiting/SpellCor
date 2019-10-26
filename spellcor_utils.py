import os


def maybe_mkdir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def token_string(sentence):
    """根据空格 和 所有非字母把句子分割成list,不删除空格方便还原文本，
        后处理时，可以删除多余空格。
        输入 为 string
        返回 对 element 做lower 的列表， 和不做lower 的列表 方便 capital 单词
        call: token_string("Hello Word k'w Waht be the one")
        return: (['Hello', ' ', 'Word', ' ', 'k', "'", 'w', ' ', 'Waht', ' ', 'be', ' ', 'the', ' '],
                ['hello', ' ', 'word', ' ', 'k', "'", 'w', ' ', 'waht', ' ', 'be', ' ', 'the', ' '])
    """
    tokenized_list = []
    alphas, symbols = [], []
    special_symbols = [" "]
    for char in sentence:
        if char in special_symbols:
            if alphas: tokenized_list.append("".join(alphas))
            if symbols: tokenized_list.append("".join(symbols))
            alphas, symbols = [], []
            tokenized_list.append(char)
        elif char.isalpha():
            alphas.append(char)
            if symbols:
                tokenized_list.append("".join(symbols))
                symbols = []
        else:
            symbols.append(char)
            if alphas:
                tokenized_list.append("".join(alphas))
                alphas = []
    else:
        if char.isalpha():
            tokenized_list.append("".join(alphas))
        elif char not in special_symbols:
            tokenized_list.append("".join(symbols))
    lower_tokenized_list = [t.lower() for t in tokenized_list]
    # print(lower_tokenized_list)
    return tokenized_list, lower_tokenized_list


def align_capital(word1, word2):
    word2 = list(word2)
    word1 = list(word1)
    for i in range(len(word2)):
        k = i if i<len(word1) else len(word1)-1
        if word1[k].lower() == word2[i] and word1[k].isupper():
            word2[i] = word2[i].upper()
    return "".join(word2)


def delete_1(word):
    results = set()
    for i in range(len(word)):
        new_w = word[:i] + word[i + 1:]
        if new_w:
            results.add(new_w)
    return results


def delete_2(word):
    results = set()
    for i in range(len(word)):
        new_w = word[:i] + word[i + 1:]
        if new_w:
            results.update(delete_1(new_w))
            results.add(new_w)
    return results


def insert_1(alphas,word,is_word):
    results = set()
    for i in range(len(word)+1):
        for alpha in alphas:
            new_w = word[:i]+alpha+word[i:]
            # new_w = word
            if is_word(new_w):
                results.add(new_w)
    return results


def insert_2(alphas, word, is_word, delete_1):
    results = set()
    for i in range(len(word) + 1):
        for alpha in alphas:
            new_w = word[:i] + alpha + word[i:]
            if new_w not in delete_1:
                results.update(insert_1(alphas, new_w, is_word))
                if is_word(new_w):results.add(new_w)
    return results


# TO-DO: optimize this function
# costly function, if running annotated code
# currently version sacrifices some performance to decrease the time
def edit_distance_2(alphas, word, is_word):
    candidates = set()
    cands = delete_2(word)
    cands_1 = delete_1(word)
    for c in cands:
        if is_word(c): candidates.add(c)
        candidates.update(insert_1(alphas, c, is_word)) # not optimal in performance, but fast
        # elif c in cands_1:
        #     candidates.update(insert_1(alphas, c, is_word))
        # else:
        #     candidates.update(insert_2(alphas, c, is_word, cands_1))
    return list(candidates)


def edit_distance_1(alphas, word, is_word, last_level=True):
    candidates = []
    for i in range(len(word)+1):
        # insert
        for alpha in alphas:
            candidate = word[:i]+alpha+word[i+1:]
            if is_word(candidate): candidates.append(candidate)
            if not last_level: candidates.extend(edit_distance_1(alphas, candidate, True))
        # delete
        if i<len(word):
            candidate = word[:i]+word[i+1:]
            if is_word(candidate): candidates.append(candidate)
            if not last_level: candidates.extend(edit_distance_1(alphas, candidate, True))
        # transpose
        if i < len(word)-1:
            candidate = word[:i]+word[i+1]+word[i]+word[i+2:]
            if is_word(candidate): candidates.append(candidate)
            if not last_level: candidates.extend(edit_distance_1(alphas, candidate, True))
        # replace
        if i<len(word):
            for alpha in alphas:
                candidate = word[:i]+alpha+word[i+1:]
                if is_word(candidate): candidates.append(candidate)
                if not last_level: candidates.extend(edit_distance_1(alphas, candidate, True))
    return list(set(candidates))


if __name__ == "__main__":
    print(token_string("Hello Word k'w Waht be the one"))
    print(edit_distance_2("evaluetde"))

