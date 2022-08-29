import inflect
import spacy
import csv
import sys
import en_core_web_lg


nlp = en_core_web_lg.load()
p = inflect.engine()

# Add to list function to add the list of significant scores to list
def addToList(ele, lst, num_ele):
    if ele in lst:
        return lst
    if len(lst) >= num_ele:  # if list is at capacity
        if ele[1] > float(lst[-1][1]):  # if element's sig_score is larger than smallest sig_score in list
            lst.pop(-1)
            lst.append((ele[0], str(ele[1])))
            lst.sort(key=lambda x: float(x[1]), reverse=True)
    else:
        lst.append((ele[0], str(ele[1])))
        lst.sort(key=lambda x: float(x[1]), reverse=True)
    return lst

import json

# list of English vocabs
en_vocab = []
file = open("merged.txt")
csvreader = csv.reader(file)
for row in csvreader:
    w = p.singular_noun(row[0])
    if w:
        en_vocab.append(w)
    else:
        en_vocab.append(row[0])

# tokenizing the words in the vocab list
tokens = nlp(' '.join(en_vocab))

# initiate empty dictionary to store the results
en_dict = {}

# Nested for loop to calculate cosine similarity scores
f = open("similarities_trf.csv", 'w')
writer = csv.writer(f)
for i in range(0, len(tokens) - 1):
    word1 = tokens[i]
    print('Processing for ' + word1.text + ' (' + str(i) + ' out of ' + str(len(tokens)) + ' words)')
    for j in range(i + 1, len(tokens)):
        word2 = tokens[j]
        similarity = word1.similarity(word2)
        item = [word1.text, word2.text, similarity]
        writer.writerow(item)
    if i > 0:
        break

sys.exit()

# Nested for loop to calculate cosine similarity scores
for i in range(len(en_vocab)):
    word = en_vocab[i]
    print('Processing for ' + word + ' (' + str(i) + ' out of ' + str(len(en_vocab)) + ' words)')
    for j in range(i + 1, len(en_vocab)):
        try:
            prev_list_i = en_dict[str(tokens[i])]['similar_words']
        except Exception as e:
            prev_list_i = []
        en_dict[str(tokens[i])]['similar_words'] = addToList((str(tokens[j]), tokens[i].similarity(tokens[j])), prev_list_i, 100)
        prev_list_j = en_dict[str(tokens[j])]['similar_words']
        en_dict[str(tokens[j])]['similar_words'] = addToList((str(tokens[i]), tokens[i].similarity(tokens[j])), prev_list_j, 100)

    with open('data.json', 'w') as f:
        json.dump(en_dict, f)
