import os

with open(os.path.join('data', 'filtered_words.csv'), 'r') as f:
    # skip headers
    f.readline()
    with open(os.path.join('data', 'new_pangram_sets.txt'), 'w') as newset:
        for line in f:
            line = line.rstrip()
            letters, required, _, _ = line.split(',')
            newset.write(f'{letters},{required}\n')