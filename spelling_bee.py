import random
import os
import json
import couchdb
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, session

# -----------------------------------------------------------
# user database
# -----------------------------------------------------------
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
    def today_game(self):
        today = str(date.today())
        today_record = self.word_db.get(today)

        if today_record is not None:
            return today_record
        
        with open(os.path.join('data', 'pangram_sets.txt'), 'r') as f:
            pangram_sets = [set(x.strip()) for x in f]
        pangram_set = random.choice(pangram_sets)
        required_letter = random.choice(tuple(pangram_set))

        with open(os.path.join('data', 'words.txt'), 'r') as f:
            all_words = [x.strip() for x in f]
        word_list = tuple([x for x in all_words if pangram_set.union(set(x)) == pangram_set and required_letter in x])

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
            return yesterday_game.get('word_list')
        else:
            return False
        


# -----------------------------------------------------------
# game mechanics
# -----------------------------------------------------------
class GameState:
    def __init__(self):
        self.db = Database()
        self._letter_set = None
        self._required = None
        self._words = None
        self._last_updated = None

    @property
    def letter_set(self):
        if self._letter_set is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self._letter_set = set(self.db.today_game['hive_letters'])
            self._last_updated = datetime.now()

        return self._letter_set

    @property
    def required(self):
        if self._required is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self._required = self.db.today_game['queen_letter']
            self._last_updated = datetime.now()

        return self._required
    
    @property
    def words(self):
        if self._words is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self._words = self.db.today_game['word_list']
            self._last_updated = datetime.now()

        return self._words

    @property
    def yesterday_words(self):
        if self.db.yesterday_words:
            return self.db.yesterday_words
        else:
            return ['No words yesterday.']

    @property
    def maximum_score(self):
        if 'max_score' in self.db.today_game:
            return self.db.today_game['max_score']
        
        max_score = sum(self.score_word(x) for x in self.db.today_game['word_list'])
        self.db.today_game['max_score'] = max_score
        return max_score

    @property
    def thresholds(self):
        return {
            'Beginner': 0,
            'Good Start': round(0.02 * self.maximum_score),
            'Moving Up': round(0.05 * self.maximum_score),
            'Good': round(0.08 * self.maximum_score),
            'Solid': round(0.15 * self.maximum_score),
            'Nice': round(0.25 * self.maximum_score),
            'Great': round(0.40 * self.maximum_score),
            'Amazing': round(0.50 * self.maximum_score),
            'Genius': round(0.70 * self.maximum_score),
            'Queen Bee': self.maximum_score
        }


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

# -----------------------------------------------------------
# flask app
# -----------------------------------------------------------
app = Flask(
    __name__,
    static_folder=os.path.join('dist', 'static'),
    template_folder='dist')
try:
    app.secret_key = os.environ['SECRET_KEY']
except KeyError:
    app.logger.warning('$SECRET_KEY not in environment.')
    app.secret_key = 'BAD_SECRET_KEY_FOR_DEVELOPMENT'

game_state = GameState()
app.logger.debug(game_state.words)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

def get_setup(session):
    to_return = {
        'required': game_state.required,
        'letters': list(game_state.letter_set),
        'thresholds': list(game_state.thresholds.keys()),
        'score_levels': list(game_state.thresholds.values()),
        'num_words': len(game_state.words),
        'yesterday_words': game_state.yesterday_words
    }

    if session.get('letters') != list(game_state.letter_set):
        session['letters'] = list(game_state.letter_set)
        session['score'] = 0
        session['already_guessed'] = []

    if 'score' in session:
        to_return['score'] = session['score']
    else:
        session['score'] = 0
        to_return['score'] = 0

    if 'already_guessed' in session:
        to_return['already_guessed'] = session['already_guessed']
    else:
        session['already_guessed'] = []
        to_return['already_guessed'] = []

    return to_return

def check_word(session, word):
    score = game_state.score_word(word.lower())
    if score != 0:
        temp = session['score']
        temp += score
        session['score'] = temp

        temp = session['already_guessed']
        temp.append(word.lower())
        session['already_guessed'] = temp

    return {'score': score}

@app.route('/api', methods = ['POST'])
def api():
    global game_state
    rj = request.get_json()

    if rj['action'] == 'get_setup':
        return json.dumps(get_setup(session)), 200, {'ContentType': 'application/json'}

    if rj['action'] == 'check_word':
        return json.dumps(check_word(session, rj['word'])), 200, {'ContentType': 'application/json'}