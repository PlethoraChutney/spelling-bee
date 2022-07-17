import couchdb
import os
import random
from datetime import date, timedelta

class Database:
    def __init__(self) -> None:
        host = os.environ['COUCHDB_HOST']
        username = os.environ['COUCHDB_USERNAME']
        password = os.environ['COUCHDB_PASSWORD']
        self.server = couchdb.Server(f'http://{username}:{password}@{host}:5984')

        if 'word_lists' in self.server:
            self.word_db = self.server['word_lists']
        else:
            self.word_db = self.server.create('word_lists')

        if 'spelling_bee_users' in self.server:
            self.user_db = self.server['spelling_bee_users']
        else:
            self.user_db = self.server.create('spelling_bee_users')

    @property
    def today_game(self) -> dict:
        today = str(date.today())
        today_record = self.word_db.get(today)

        if today_record is not None:
            return today_record
        
        with open(os.path.join('data', 'new_pangram_sets.txt'), 'r') as f:
            game_sets = [x.strip() for x in f]
        game_set = random.choice(game_sets)
        pangram_set, required_letter = game_set.split(',')
        pangram_set = set(pangram_set)

        with open(os.path.join('data', 'words.txt'), 'r') as f:
            all_words = [x.strip() for x in f]
        word_list = [x for x in all_words if pangram_set.union(set(x)) == pangram_set and required_letter in x]

        pangram_set.remove(required_letter)

        game_dict = {
            'hive_letters': list(pangram_set),
            'queen_letter': required_letter,
            'word_list': word_list
        }

        self.word_db[today] = game_dict
        return self.word_db[today]

    @property
    def yesterday_words(self):
        yesterday = str(date.today() - timedelta(days = 1))
        yesterday_game = self.word_db.get(yesterday)
        if yesterday_game is not None:
            word_list = yesterday_game.get('word_list')
            return word_list
        else:
            return False
 

db = Database()

print(db.today_game)