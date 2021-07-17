import urllib.request # Built-in Python 3 library (https://docs.python.org/3/library/urllib.html) 
import itertools # Built-in Python 3 library (https://docs.python.org/3/library/itertools.html)
import platform # Built-in Python 3 library (https://docs.python.org/3/library/platform.html)
import os # Built-in Python 3 library (https://docs.python.org/3/library/os.html)

def clear():
    system = platform.system()
    if system == "Windows":
        os.system("cls")
    elif system == "Linux":
        os.system("clear")
    else:
        pass

words = urllib.request.urlopen("https://raw.githubusercontent.com/dwyl/english-words/master/words.txt") # list of words in the English language, created by DWYL (https://github.com/dwyl) 
words = words.read().decode("utf-8") # reads the web response and decodes the bytes of the web response into text
words = words.split("\n") # splits the content by lines into individual words

checklist = urllib.request.urlopen("https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt") # list of commonly searched English words, created by first20hours (https://github.com/first20hours/)
checklist = checklist.read().decode("utf-8") # reads the web response and decodes the bytes of the web response into text
checklist = checklist.split("\n") # splits the content by lines into individual words

alphabet = "qwertyuiopasdfghjklzxcvbnm" # string containing all letters in english alphabet (not required to be in order)
def sanitize(word):
    for letter in word:
        if letter not in alphabet:
            return False
    return True

words = [word for word in words if sanitize(word)] # sanitizes the word list, as Scrabble doesn't score nor count punctuation marks
loweredwords = [w.lower() for w in words]

#checklist = ["test"]
#words = ([word for word in words if word in checklist]) # compares word list to commonly searched words, removes uncommon/not allowed words

def score(word):
    values = {"lsunrtoaie": 1, "dg": 2, "bcmp": 3, "fhvwy": 4, "k": 5, "jx": 8, "qz": 10}
    value = 0
    for letter in word:
        key = [k for k in values.keys() if letter in k][0]
        value += values[key]
    return value

def find_best(letters, target):
    #best_score = -float("inf") # lowest numerical value in Python, negative infinity
    
    found_words = [] # list of found words, given the letter

    max_length = len(letters) # limit on the word length 

    for l in range(max_length-1):
        l = l + 3 # range starts at 0, by subtracting 1 and adding 3 a minimum length of 3 can be set while still maintaining the maximum length
        word_set = set(["".join(sorted(word)) for word in set(itertools.permutations(letters, l))]) # removes duplicates from the initial permutation generator, then sorts every permutation and puts them all in a list, then removes duplicate sorted permutations - the result is an iterable filled with unique letter combinations
        
        potential_words = [word for word in words if "".join(sorted(word)) in word_set] # list comprehension is used to save time, as list comprehension is faster than using for-loops to traverse through all of the elements in word_set and append them to a new list if they fit a certain requirement
        
        potential_words = []
        for word in checklist:
            if "".join(sorted(word)) in word_set:
                potential_words.append(word)
        
        found_words = found_words + potential_words
    
    found_words = [w for w in found_words if target in w] # filters the list for elements that contain the target letter

    scores = {word: score(word) for word in found_words}
    
    scores = {k: v for k, v in sorted(scores.items(), key=lambda x: x[1], reverse=True)}
    return scores

while True:
    clear()
    letters = input("Letters in hand: ")
    target = input("Target (required) letter: ")
    clear()
    print("Finding...")
    scores = find_best(letters, target)
    to_print = ""
    clear()
    print("Top {} words:".format(min(10, len(list(scores.keys())))))
    for i, word in enumerate(list(scores.keys())[:10]):
        to_print = to_print + "\n{}: {} (scores {})".format(i+1, word, scores[word])
    to_print = to_print.lstrip()
    print(to_print)
    input("Press enter to continue. ")