import os
import pandas as pd

def score_word(word, pangram) -> int:
    if len(word) < 4:
        return 0
    if len(word) == 4:
        return 1
    else:
        score = len(word)

    if set(word) == pangram:
        score += 7

    return score

with open(os.path.join('data', 'pangram_sets.txt'), 'r') as f:
    pangram_sets = [set(x.strip()) for x in f]

total_scores = []

with open(os.path.join('data', 'words.txt'), 'r') as f:
    all_words = [x.strip() for x in f]

while pangram_sets:
    pangram_set = pangram_sets.pop()

    required_from = pangram_set
    if pangram_set.intersection({'i', 'n', 'g'}) == {'i', 'n', 'g'}:
        required_from = required_from - {'i', 'n', 'g'}
    if pangram_set.intersection({'e', 'd'}) == {'e', 'd'}:
        required_from = required_from - {'e', 'd'}
    if pangram_set.intersection({'e', 'r'}) == {'e', 'r'}:
        required_from = required_from - {'e', 'r'}

    required_from = list(required_from)

    while required_from:
        required_letter = required_from.pop()
        word_list = tuple([x for x in all_words if pangram_set.union(set(x)) == pangram_set and required_letter in x])
        score = sum(score_word(x, pangram_set) for x in word_list)
        total_scores.append({
            'letters': ''.join(list(pangram_set)),
            'required': required_letter,
            'score': score,
            'words': len(word_list)
        })

pd.DataFrame(total_scores).to_csv('all_scores.csv', index=False)