import markovify

def load(path):
    with open(path, "r", encoding="utf8") as f:
        text = f.read()
    corpus = text.split("\n")
    #corpus = [word for word in line for line in corpus if (len(word.strip()) > 0 and not word.startswith("!") and not word.startswith(".") and not word.startswith("t!") and not word.startswith("u!"))]
    corpus = [line for line in corpus if len(line.split(" ")) > 0]
    corpus = corpus[-100000:]
    global text_model
    text_model = markovify.Text(corpus)

def syllable_count(word):
    word = word.lower()
    count = 0
    vowels = "aeiouy"
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def generate():
    try:
        _ = text_model
    except:
        raise ValueError("path to text file has not been loaded")
    haiku = ""
    making = True
    index = 0
    while making:
        line = text_model.make_sentence()
        if line is None:
            continue
        syllables = 0
        for word in line.split(" "):
            syllables += 1
        if syllables == 5 and index == 0:
            haiku += line + "\n"
            index += 1
        elif syllables == 7 and index == 1:
            haiku += line + "\n"
            index += 1
        elif syllables == 5 and index == 2:
            haiku += line + "\n"
            making = False
    print(haiku)