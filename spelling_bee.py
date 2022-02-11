import random
import os
import json
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request, session

# -----------------------------------------------------------
# game mechanics
# -----------------------------------------------------------
class GameState:
    def __init__(
        self, letter_set: set, required: str,
        words: tuple, date_created:date = date.today(),
        yesterday_words:list = [None],
        ):
        self.letter_set = letter_set
        self.required = required
        self.words = words
        self.created = date_created
        self.yesterday_words = yesterday_words

        self.maximum_score = sum(self.score_word(x) for x in self.words)
        self.thresholds = {
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

    @property
    def game_age(self) -> int:
        return (date.today() - self.created).days
        
    @staticmethod
    def make_new_game(json_file = None):
        if json_file is None:
            with open(os.path.join('data', 'pangram_sets.txt'), 'r') as f:
                pangram_sets = [set(x.strip()) for x in f]
            pangram_set = random.choice(pangram_sets)
            required_letter = random.choice(tuple(pangram_set))

            with open(os.path.join('data', 'words.txt'), 'r') as f:
                all_words = [x.strip() for x in f]
            word_list = tuple([x for x in all_words if pangram_set.union(set(x)) == pangram_set and required_letter in x])

            pangram_set.remove(required_letter)
            return GameState(pangram_set, required_letter, word_list)
        else:
            app.logger.info('Reading from JSON file')
            with open(json_file, 'r') as f:
                letter_sets = json.load(f)

            today, yesterday = list(letter_sets.keys())

            date_created = datetime.strptime(today, '%Y-%m-%d').date()

            letter_set = set(letter_sets[today]['letter_set'])
            required_letter = letter_sets[today]['required_letter']
            if 'word_list' in letter_sets[today]:
                word_list = letter_sets[today]['word_list']
            else:
                total_set = letter_set
                total_set.add(required_letter)
                with open(os.path.join('data', 'words.txt'), 'r') as f:
                    word_list = [x.rstrip() for x in f if total_set.union(set(x.rstrip())) == letter_set and required_letter in x.rstrip()]


            return GameState(
                letter_set, required_letter, word_list,
                date_created = date_created, yesterday_words = letter_sets[yesterday]['words']
            )
        
    def write_to_json(self):
        yesterday = self.created - timedelta(days = 1)
        to_write = {
            str(self.created): {
                'letter_set': list(self.letter_set),
                'required_letter': self.required,
                'word_list': self.words
            },
            str(yesterday): {
                'words': self.yesterday_words
            }
        }

        with open('game_state.json', 'w') as f:
            json.dump(to_write, f)

    def cycle_game(self):
        new_game = GameState.make_new_game()
        new_game.yesterday_words = self.words

        new_game.write_to_json()
        return new_game


    def score_word(self, word: str) -> int:
        app.logger.debug(word + ' ' + str(len(word)))
        app.logger.debug('In list: ' + str(word in self.words))
        app.logger.debug('Required in word: ' + str(self.required in word))
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

try:
    game_state = GameState.make_new_game('game_state.json')
except FileNotFoundError:
    game_state = GameState.make_new_game()
app.logger.debug(game_state.words)

@app.route('/', methods = ['GET'])
def index():
    global game_state
    if game_state.game_age > 0:
        game_state = game_state.cycle_game()

    return render_template('index.html')

@app.route('/api', methods = ['POST'])
def api():
    global game_state
    rj = request.get_json()

    if rj['action'] == 'get_setup':
        to_return = {
            'required': game_state.required,
            'letters': list(game_state.letter_set),
            'thresholds': list(game_state.thresholds.keys()),
            'score_levels': list(game_state.thresholds.values()),
            'num_words': len(game_state.words)
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

        return json.dumps(to_return), 200, {'ContentType': 'application/json'}

    if rj['action'] == 'check_word':
        score = game_state.score_word(rj['word'].lower())
        if score != 0:
            temp = session['score']
            temp += score
            session['score'] = temp

            temp = session['already_guessed']
            temp.append(rj['word'].lower())
            session['already_guessed'] = temp

        return json.dumps({'score': score}), 200, {'ContentType': 'application/json'}