from spelling_bee import GameState
import pandas as pd
import os

# We need to calculate what our max scores and number of words
# would be for all these old NYT games. Then we can fit a function
# (I'll use R haha) from which we can generate tresholds for our
# games. Data from https://github.com/wchargin/spelling-bee

prev_thresholds = pd.read_csv(
    os.path.join('data', 'ratings-20160103-20180304.csv'),
    names=['required', 'optional', 'good', 'excellent', 'genius', 'date'],
    skiprows = 7
)

print(prev_thresholds)

def get_scores(row):
    game = GameState.make_new_game(
        required_letter=row['required'],
        pangram_set=set(list(row['optional'] + row['required'])))

    return len(game.words), game.maximum_score

prev_thresholds['Jump'] = prev_thresholds['excellent'] - prev_thresholds['good']
prev_thresholds['words_score'] = prev_thresholds.apply(get_scores, axis = 1)

prev_thresholds.to_csv(
    os.path.join('data', 'calculated_scores.csv'), index = False
)
