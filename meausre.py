import spellcor

checker = spellcor.SpellChecker()
checker.load_lang_model("BaseLanguageModel", "./tmp/nglm.bin")
input_file = "./data/spell_test_orig.txt"
input_sentences = []
with open(input_file, 'r', encoding="utf-8") as f:
    input_sentences = f.readlines()

hypo_sentence = []

for i,sen in enumerate(input_sentences):
    if i%1000 == 0:
        print("{}/{}".format(i,len(input_sentences)))
    hypo_sentence.append(checker.fix_sentence(sen.strip()))

hypo_file = "./data/spell_test_hypo.txt"
with open(hypo_file,'w', encoding="utf-8") as f:
    for sen in hypo_sentence:
        f.write(sen+"\n")


