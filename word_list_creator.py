with open('words.txt', 'r') as f:
    all_words = [x.strip() for x in f]

all_words = [x for x in all_words if 's' not in x]

pangram_sets = [set(x) for x in all_words if len(set(x)) == 7]

# unique is the list of all sets of letters which have a pangram
unique = [x for x in set(frozenset(y) for y in pangram_sets)]

with open('pangram_sets.txt', 'w') as f:
    for letters in unique:
        f.write(''.join(list(letters)))
        f.write('\n')