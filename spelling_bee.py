import random
import os
from datetime import date

class GameState:
    def __init__(self, letter_set: set, required: str, words: tuple):
        self.letter_set = letter_set
        self.required = required
        self.words = words
        self.created = date.today()

        self.maximum_score = sum(self.score_word(x) for x in self.words)

    @property
    def game_age(self) -> int:
        return (date.today() - self.created).days
        
    @staticmethod
    def make_new_game(pangram_set = None, required_letter = None):
        if pangram_set is None:
            with open(os.path.join('data', 'pangram_sets.txt'), 'r') as f:
                pangram_sets = [set(x.strip()) for x in f]
            pangram_set = random.choice(pangram_sets)
        else:
            pangram_set = set(pangram_set)
            assert len(pangram_set) == 7, 'Must pick seven letter pangram set'

        if required_letter is None:
            required_letter = random.choice(tuple(pangram_set))
        else:
            assert required_letter in pangram_set, 'Must pick required letter from pangram set'

        with open(os.path.join('data', 'words.txt'), 'r') as f:
            all_words = [x.strip() for x in f]
        word_list = tuple([x for x in all_words if pangram_set.union(set(x)) == pangram_set and required_letter in x])

        return GameState(pangram_set, required_letter, word_list)

    def score_word(self, word: str) -> int:
        if word not in self.words or len(word) < 4 or self.required not in word:
            return 0

        if len(word) == 4:
            score = 1
        else:
            score = len(word)

        if self.letter_set.intersection(set(word)) == self.letter_set:
            score += 7

        return score


new_game = GameState.make_new_game()
print(new_game.words[0], new_game.score_word(new_game.words[0]))
print(len(new_game.words), new_game.maximum_score)
