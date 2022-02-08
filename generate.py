import re
import os
import networkx as nx
from random import randint

WORD_LENGTH = 5

with open('words.txt', 'r') as fp:
    allowed_words = fp.readlines()
allowed_words = [x.strip() for x in allowed_words if len(x.strip()) == 5]
print(f'Number of words: {len(allowed_words)}')
with open('dictionary.txt', 'r') as fp:
    dictionary_words = fp.readlines()
dictionary_words = [x.strip().upper() for x in dictionary_words if len(x.strip()) == 5]
if not os.path.isfile('dictionary_5.txt'):
    with open('dictionary_5.txt', 'w') as fp:
        fp.write('\n'.join(dictionary_words))
allowed_words = [x.upper() for x in allowed_words if x.upper() in dictionary_words]
print(f'Number of *dictionary* words: {len(allowed_words)}')
allowed_words = allowed_words[:1000]

def import_text(filename):
    text_arr = []
    with open(filename, 'r') as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            text_arr.append(line)


    print(len(text_arr))
    text_arr = [x for x in text_arr if len(x) > 1]
    # text_arr = [x for x in text_arr if not x[0].isnumeric()]
    text_arr = [x.strip(' ') for x in text_arr]
    print(len(text_arr))

    print(text_arr[:3])

    text = ''.join(text_arr)
    # text = text.replace('-', '')
    text = text.replace('\n', ' ')
    text = re.sub(r'\s\s+', ' ', text)

    print(text[:100])
    return text

def find_matches(text):
    matches = re.findall(r'(\s+[A-Z][^.!?\d"]{40,50}[.!?])', text)
    for match in matches[:5]:
            print(f'Example: {match}')
    print(f'Found {len(matches)} matches')
    return matches

def find_word(text):
    words = []
    G = nx.DiGraph()
    # text = re.sub(r'[^A-Za-z]', '', text)
    text = text.strip()
    for i in range(len(text)):
        for j in range(i, len(text)):
            if text[i] != ' ' and text[j] != ' ':
                G.add_edge(i, j)


    allowed_words_without_dups = [x for x in allowed_words]
    # print(allowed_words_without_dups)
    start_range = randint(2, 15)
    end_range = randint(2, 17-start_range)
    for i in range(start_range):
        for j in range(end_range):
            target = len(text)-1-j
            if G.has_node(i) and G.has_node(j) and G.has_node(target):
                for path in nx.all_simple_paths(G, i, target, cutoff=5):
                    if len(path) != 5:
                        continue
                    word = ''
                    for loc in path:
                        word += text[loc]
                    # print(word)
                    if word in allowed_words_without_dups:
                        # print(word)
                        words.append(','.join([str(x) for x in path]) + '|' + word)
                        allowed_words_without_dups.remove(word)
                        if len(words) > 25:   # just to reduce runtime
                            return words
    return words

    
        



clues = []
if os.path.isfile('answers.txt'):
    with open('answers.txt', 'r') as fp:
        answers = fp.readlines()
        clues = [x.split('|')[0] for x in answers]

text = import_text('dracula.txt')
matches = find_matches(text)
for sentence in matches[:100]:
    if sentence in clues:
        continue
    found_words = find_word(sentence.upper())
    if len(found_words) == 0:
        continue
    answer = found_words[randint(0, len(found_words)-1)]
    while answer in sentence:
        answer = found_words[randint(0, len(found_words)-1)]
    # print(f'Clue: {sentence}\nAnswer: {answer}')
    with open('answers.txt', 'a') as fp:
        a = f'{sentence}|{answer}\n'
        fp.write(a.upper())



