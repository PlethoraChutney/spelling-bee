<template>
  <SpellingBee
  :letters="letters"
  :required="required"
  @shuffle-letters="shuffleLetters()"
  @check-word="checkWord($event)"/>
</template>

<script>
import SpellingBee from './components/SpellingBee.vue'

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
    SpellingBee
  },
  data() {
    return {
      'letters': ['','','','','',''],
      'required': '',
      'score': 0,
      'previousWords': []
    }
  },
  created() {
    document.title = 'Spelling Bee';

    sendRequest({'action': 'get_setup'})
      .then(request => request.json()
        .then(data => {
          this.letters = data.letters;
          this.required = data.required;
          this.score = data.score;
          this.previousWords = data.already_guessed;
        })
      )
  },
  methods: {
    showMessage(message) {
      console.log(message);
    },
    shuffleLetters() {
      this.letters = shuffle(this.letters);
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
            this.previousWords.sort();
          }
        }))
    }
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
}
</style>
