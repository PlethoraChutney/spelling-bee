<template>
  <h1 id="title">Lindsey's Spelling Bee</h1>
  <div id="game-side" class="v-center">
    <SpellingBee
    :letters="letters"
    :message="message"
    :required="required"
    :shuffling="shuffling"
    :clearWord="clearWord"
    @shuffle-letters="shuffleLetters()"
    @check-word="checkWord($event)"/>
  </div>
  <div id="score-side" class="v-center">
    <ScoreBar
    :score="score"
    :thresholds="thresholds"
    :scoreLevels="scoreLevels"
    />
    <WordList
    :wordList="previousWords"
    :numWords="numWords"
    />
  </div>
</template>

<script>
import SpellingBee from './components/SpellingBee.vue'
import WordList from './components/WordList.vue'
import ScoreBar from './components/ScoreBar.vue'

function sendRequest(body) {
    return fetch('/api', {
        method: 'POST',
        mode: 'cors',
        cache: 'no-cache',
        credentials: 'same-origin',
        headers: {
            'Content-Type': 'application/json'
        },
        redirect: 'follow',
        referrerPolicy: 'no-referrer',
        body: JSON.stringify(body)
    })
}

function shuffle(array) {
  let currentIndex = array.length,  randomIndex;

  // While there remain elements to shuffle...
  while (currentIndex != 0) {

    // Pick a remaining element...
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex], array[currentIndex]];
  }

  return array;
}

export default {
  name: 'App',
  components: {
    SpellingBee,
    WordList,
    ScoreBar
  },
  data() {
    return {
      'letters': ['','','','','',''],
      'thresholds': ['Beginner'],
      'scoreLevels': [0],
      'numWords': 1,
      'shuffling': false,
      'required': '',
      'score': 0,
      'previousWords': [],
      'message': '',
      'clearWord': false
    }
  },
  created() {
    document.title = 'Spelling Bee';

    sendRequest({'action': 'get_setup'})
      .then(request => request.json()
        .then(data => {
          this.letters = data.letters;
          this.thresholds = data.thresholds;
          this.scoreLevels = data.score_levels;
          this.numWords = data.num_words;
          this.required = data.required;
          this.score = data.score;
          this.previousWords = data.already_guessed;
        })
      )
  },
  methods: {
    showMessage(message) {
      this.message = message;
      window.setTimeout(() => {
        this.clearWord = true;
        window.setTimeout(() => {
          this.clearWord = false;
        }, 100);
      }, 500);
      window.setTimeout(() => {
        this.message = '';
      }, 1500);
    },
    shuffleLetters() {
      this.shuffling = true;
      window.setTimeout(() => {
        this.letters = shuffle(this.letters);
      }, 400);
      window.setTimeout(() => {
        this.shuffling = false;
      }, 800);
    },
    checkWord(wordArray) {
      let word = [];
      wordArray.forEach(e => {
        word.push(e['letter'])
      });

      let allowedLetters = []
      word.forEach(letter => {
        letter = letter.toLocaleLowerCase()
        allowedLetters.push(this.letters.includes(letter) || this.required === letter)
      })
      if (!allowedLetters.every(e => e === true)) {
        this.showMessage('Forbidden letters');
        return false;
      }

      word = word.join('').toLocaleLowerCase();

      if (this.previousWords.includes(word)) {
        this.showMessage(`Already guessed ${word}`);
        return false;
      } else if (word.length < 4) {
        this.showMessage('Too short')
        return false;
      } else if (!word.includes(this.required)) {
        this.showMessage(`Missing "${this.required.toLocaleUpperCase()}"`);
        return false;
      }

      sendRequest({
        'action': 'check_word',
        'word': word
        }).then(request => request.json()
        .then(data => {
          if (data.score === 0) {
            this.showMessage('Not a word.');
          } else {
            this.score += data.score;
            this.previousWords.push(word);
            this.showMessage(`Nice! +${data.score}`)
          }
        }))
    }
  }
}
</script>

<style>
@import url('https://fonts.googleapis.com/css2?family=Lato:wght@400;900&display=swap');

body {
  overflow: hidden;
}

#app {
  font-family: Lato, Avenir, Helvetica, Arial, sans-serif;
  font-weight: 400;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2f2f2f;
  display: grid;
  grid-template-rows: 75px 1fr;
  grid-template-columns: 1fr 1fr;
  grid-template-areas: "title title" "game score";
  height: 100vh;
  padding: 0;
}

@media screen and (max-width: 650px) {
  #app {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
  }

  body {
    overflow-y: scroll;
    scrollbar-width: none;
  }

  h1 {
    display: none;
    visibility: hidden;
  }
}

#title {
  grid-area: title;
  border-bottom: 3px solid #2f2f2f;
  padding-bottom: 20px;
  margin-bottom: 0;
}

#game-side {
  grid-area: game;
}

#score-side {
  grid-area: score;
}

.v-center {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

</style>
