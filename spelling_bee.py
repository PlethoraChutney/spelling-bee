import random
import sys
import os
import json
import couchdb
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
from flask_login import LoginManager, UserMixin, login_user, current_user
from hashlib import sha256

# -----------------------------------------------------------
# user and word database
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

    def get_user(self, user_id):
        if user_id in self.user_db:
            return User(user_id, self.user_db)
        else:
            return None

    def authenticate_user(self, user_id, secret_word) -> str:
        user_info = self.get_user(user_id)
        
        if user_info is None:
            return 'no user'


        secret_word = sha256(secret_word.encode('utf-8')).hexdigest()
        
        app.logger.debug(f'Authenticating user {user_info.id}')
        app.logger.debug(f'Submitted hash: {secret_word}')
        app.logger.debug(f'Stored hash: {user_info.user_doc["secret_word"]}')

        if secret_word == user_info.user_doc['secret_word']:
            app.logger.debug('Match')
            return 'success'
        else:
            app.logger.debug('Mismatch')
            return 'bad password'

    def create_user(self, user_id) -> str:
        if user_id in self.user_db:
            return 'user exists'

        with open(os.path.join('data', 'words.txt'), 'r') as f:
            all_words = [x.strip() for x in f]

        secret_word = random.choice(all_words)
        secret_hash = sha256(secret_word.encode('utf-8')).hexdigest()
        
        self.user_db[user_id] = {
            'secret_word': secret_hash,
            'games': {}
        }

        return secret_word
        
# -----------------------------------------------------------
# users
# -----------------------------------------------------------

class User(UserMixin):

    def __init__(self, user_id, db) -> None:
        super().__init__()
        self.id = user_id
        self.db = db

    @property
    def user_doc(self):
        return self.db[self.id]

    @property
    def today_game(self) -> dict:
        game = self.user_doc['games'].get(str(date.today()))
        user_doc = self.user_doc
        if game is None:
            user_doc['games'][str(date.today())] = {'found_words': []}
            self.db[self.id] = user_doc
            game = {'found_words': []}

        return game

    @property
    def found_words(self) -> list:
        return list(set(self.today_game['found_words']))

    @property
    def yesterday_found(self) -> list:
        found_words = self.user_doc['games'].get(str(date.today() - timedelta(days = 1)))
        if found_words is None:
            found_words = []
        else:
            found_words = found_words['found_words']

        return found_words

    @property
    def friends(self) -> list:
        friend_list = self.user_doc.get('friends')
        if friend_list is not None:
            return friend_list
        else:
            return []

    def add_friend(self, friend: str) -> None:
        user_doc = self.user_doc
        if 'friends' not in user_doc:
            user_doc['friends'] = []
        if friend not in user_doc['friends']:
            user_doc['friends'].append(friend)
            self.db[self.id] = user_doc

    def find_word(self, word) -> None:
        user_doc = self.user_doc
        user_doc['games'][str(date.today())]['found_words'].append(word)
        self.db[self.id] = user_doc

    def compare_word_list(self, other_user) -> list:
        return list(set(self.found_words) - set(other_user.found_words))

# -----------------------------------------------------------
# game mechanics
# -----------------------------------------------------------
class GameState:
    def __init__(self) -> None:
        self.db = Database()
        self._letter_set = None
        self._required = None
        self._words = None
        self._last_updated = None

    def update_game(self) -> None:
        self._words = self.db.today_game['word_list']
        self._required = self.db.today_game['queen_letter']
        self._letter_set = set(self.db.today_game['hive_letters'])
        self._last_updated = datetime.now()

    @property
    def letter_set(self) -> set:
        if self._letter_set is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self.update_game()

        return self._letter_set

    @property
    def required(self) -> str:
        if self._required is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self.update_game()

        return self._required
    
    @property
    def words(self) -> list:
        if self._words is None or (datetime.now() - self._last_updated).total_seconds() > 3600:
            self.update_game()

        return self._words

    @property
    def yesterday_words(self) -> list:
        if self.db.yesterday_words:
            return self.db.yesterday_words
        else:
            return ['No words yesterday.']

    @property
    def maximum_score(self) -> int:
        if 'max_score' in self.db.today_game:
            return self.db.today_game['max_score']
        
        max_score = sum(self.score_word(x) for x in self.db.today_game['word_list'])
        self.db.today_game['max_score'] = max_score
        return max_score

    @property
    def thresholds(self) -> dict:
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

    def work_together(self, user:User, coop_user_id:str) -> dict:
        return_dict = {'success': True, 'words': []}
        coop_user = self.db.get_user(coop_user_id)
        if coop_user is None:
            return_dict['success'] = False
        else:
            user.add_friend(coop_user_id)
            return_dict['words'] = list(user.compare_word_list(coop_user))

        return return_dict

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
    if app.debug:
        app.logger.warning('$SECRET_KEY not in environment.')
        app.secret_key = 'BAD_SECRET_KEY_FOR_DEVELOPMENT'
    else:
        app.logger.error('Must include secret key for production mode')
        sys.exit(1)

game_state = GameState()

if os.environ.get('BEE_SHOW_WORDS') == 'true':
    app.logger.debug(game_state.words)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return game_state.db.get_user(user_id)

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

def check_word(word):
    score = game_state.score_word(word.lower())
    if score != 0 and word not in current_user.found_words:
        current_user.find_word(word)

    return {'score': score}

@app.route('/api', methods = ['POST'])
def api():
    global game_state
    rj = request.get_json()

    if rj['action'] == 'get_setup':
        if current_user.is_authenticated:
            to_return = {
                'auth': True,
                'user_id': current_user.id,
                'friend_list': current_user.friends,
                'required': game_state.required,
                'letters': list(game_state.letter_set),
                'thresholds': list(game_state.thresholds.keys()),
                'score_levels': list(game_state.thresholds.values()),
                'num_words': len(game_state.words),
                'yesterday_words': game_state.yesterday_words,
                'score': sum(
                    [game_state.score_word(x.lower()) for x in current_user.found_words]
                    ),
                'found_words': current_user.found_words,
                'found_yesterday': current_user.yesterday_found
            }
        else:
            to_return = {'auth': False}


        return json.dumps(to_return), 200, {'ContentType': 'application/json'}

    elif rj['action'] == 'check_word':
        return json.dumps(check_word(rj['word'])), 200, {'ContentType': 'application/json'}

    elif rj['action'] == 'work_together':
        return json.dumps(game_state.work_together(current_user, rj['coop_user'])), 200, {'ContentType': 'application/json'}

@app.route('/login', methods = ['POST'])
def login():
    global game_state
    rj = request.get_json()

    if rj['action'] == 'login':
        result = game_state.db.authenticate_user(rj['user_id'], rj['secret_word'])

        if result == 'success':
            login_user(game_state.db.get_user(rj['user_id']), remember = True)
            to_return = {'success': True, 'user_id': rj['user_id']}
        else:
            to_return = {'success': False, 'reason': result}

        return json.dumps(to_return), 200, {'ContentType': 'application/json'}

    elif rj['action'] == 'create_user':
        result = game_state.db.create_user(rj['user_id'])

        if result == 'user exists':
            to_return = {'success': False, 'reason': 'user exists'}
        else:
            to_return = {'success': True, 'user_id': rj['user_id'], 'secret_word': result}
            login_user(game_state.db.get_user(rj['user_id']), remember = True)

        return json.dumps(to_return), 200, {'ContentType': 'application/json'}
