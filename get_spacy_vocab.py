import csv
from pathlib import Path
import spacy
import json
import re
import sys


IN_FOLDER = "_words"
files = Path(IN_FOLDER).glob('*.txt')
data = ""
count = 1
for file in files:
    with open(file) as fp:
        tmp = fp.read()
        data += tmp
        fp.close()
        count += 1
        if count > 1:
            pass

f = open('spacy_vocab/spacy_strings.json')
words = json.load(f)
valid_words = []
for word in words:
    if word.islower():
        if(bool(re.search('^[a-zA-Z0-9]*$', word)) is True):
            print(word)
            valid_words.append(word)

valid_word_string = " ".join(valid_words)
data = data + valid_word_string
file = "/Users/mattlavis/sites and projects/1. Online Tariff/process-hsen/commodities/commodities.csv"
with open(file) as fp:
    tmp = fp.read()
    data += tmp
    fp.close()

with open('all_hsen.txt', 'w') as fp:
    fp.write(data)
fp.close()

nlp = spacy.load("en_core_web_md")
nlp.max_length = 6927242
doc = nlp(data)

nouns = {}
extract = ""
for token in doc:
    if token.pos_ == "NOUN":
        item = token.lemma_
        if len(item) > 2:
            if 1 > 0:
                extract += item + " "
                # if(bool(re.search('^[a-zA-Z0-9]*$', word)) is True):
                if item not in nouns:
                    nouns[item] = 1
                else:
                    nouns[item] += 1


with open('prose.txt', 'w') as fp:
    fp.write(extract)
fp.close()
sys.exit()

with open('all_hsen.txt', 'w') as fp:
    for noun in nouns:
        fp.write(noun + " " + str(nouns[noun]) + "\n")

fp.close()
