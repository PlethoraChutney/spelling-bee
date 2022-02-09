import random
import os
import json
from datetime import date
from flask import Flask, render_template, request, session

# -----------------------------------------------------------
# game mechanics
# -----------------------------------------------------------
class GameState:
    def __init__(self, letter_set: set, required: str, words: tuple):
        self.letter_set = letter_set
        self.required = required
        self.words = words
        self.created = date.today()

        self.maximum_score = sum(self.score_word(x) for x in self.words)
        # these linear fits are calculated in threshold_modeler.R
        # they're not a great fit, but the best we can do for now.
        self.good_thresh = round(self.maximum_score * 0.02752295 + 3.34411497)
        self.thresh_jump = round(self.maximum_score * 0.03294177 + 1.49861706)

    @property
    def game_age(self) -> int:
        return (date.today() - self.created).days

    @property
    def thresholds(self) -> tuple:
        return (
            self.good_thresh,
            self.good_thresh + self.thresh_jump,
            self.good_thresh + 2*self.thresh_jump
        )
        
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

        pangram_set.remove(required_letter)
        return GameState(pangram_set, required_letter, word_list)

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

game_state = GameState.make_new_game()
app.logger.debug(game_state.words)

@app.route('/', methods = ['GET'])
def index():
    global game_state
    if game_state.game_age > 0:
        game_state = GameState.make_new_game()

    return render_template('index.html')

@app.route('/api', methods = ['POST'])
def api():
    global game_state
    rj = request.get_json()

    if rj['action'] == 'get_setup':
        to_return = {
            'required': game_state.required,
            'letters': list(game_state.letter_set)
        }

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