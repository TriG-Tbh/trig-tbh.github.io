import numpy as np
import random

def makepairs(corpus):
    for i in range(len(corpus)-1):
        yield (corpus[i], corpus[i+1])

def load(path):
    with open(path, "r", encoding="utf8") as f:
        text = f.read()
    global corpus, word_dict
    corpus = text.split(" ")
    corpus = [word for word in corpus if (len(word.strip()) > 0 and not word.startswith("!") and not word.startswith(".") and not word.startswith("t!") and not word.startswith("u!"))]
    corpus = corpus[:100000]
    pairs = makepairs(corpus)
    word_dict = {}
    for word_1, word_2 in pairs:
        if word_1 in word_dict.keys():
            word_dict[word_1].append(word_2)
        else:
            word_dict[word_1] = [word_2]

def getwords(word_dict, n_words, first_word):
    chain = [first_word]
    for i in range(n_words):
        yield np.random.choice(word_dict[chain[-1]])

def generate():
    try:
        _, _ = corpus, word_dict
    except:
        raise ValueError("path to text file has not been loaded")
    first_word = np.random.choice(corpus)
    n_words = 30
    chain = [first_word]
    for _ in range(n_words):
        chain.append(np.random.choice(word_dict[chain[-1]]))
    lines = (" ".join(chain)).split("\n")
    #phrase = random.choice(lines)
    #print(phrase)
    print("\n".join(lines))