import os
import re
from string import ascii_lowercase, ascii_uppercase

with open(os.path.join('data', 'words.txt'), 'r', encoding='UTF-8') as f:
    all_words = [x.strip() for x in f]

all_words = [x for x in all_words if 's' not in x and "'" not in x]

# this is slow but you only do it literally once
fixed_words = []
for word in all_words:
    # remove proper nouns
    if any([x in ascii_uppercase for x in word]):
        continue

    # remove slurs from the fucking Ubuntu dictionary
    if re.search('nigg', word) or word in ['gook', 'wetback']:
        continue

    # fix accents
    word = word.replace('é', 'e')
    word = word.replace('è', 'e')
    word = word.replace('â', 'a')
    word = word.replace('ä', 'a')
    word = word.replace('ê', 'e')
    word = word.replace('ñ', 'n')
    word = word.replace('é', 'e')
    word = word.replace('ó', 'o')
    word = word.replace('û', 'u')

    if not all([x in ascii_lowercase for x in word]):
        print(f'Unknown letter in {word}')

    fixed_words.append(word)

all_words = fixed_words

with open(os.path.join('data', 'words.txt'), 'w') as f:
    for word in all_words:
        f.write(word)
        f.write('\n')

pangram_sets = [set(x) for x in all_words if len(set(x)) == 7]

# unique is the list of all sets of letters which have a pangram
unique = [x for x in set(frozenset(y) for y in pangram_sets)]

with open(os.path.join('data', 'pangram_sets.txt'), 'w') as f:
    for letters in unique:
        f.write(''.join(list(letters)))
        f.write('\n')