<template>
  <div id="title">
    <h1>Lindsey's Spelling Bee</h1>
    <div id="yesterday-modal" class="button" @click="toggleYesterdayWordModal">Yesterday's Words</div>
  </div>
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
  <div id="score-side" class="v-center" :class="{'no-overflow': showWordModal}">
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
  <ModalWindow v-if="showWordModal"
  @toggleVisible="toggleYesterdayWordModal">
    <h1>Yesterday's Words</h1>
    <WordList
    :wordList="yesterdaysWords"
    :numWords="yesterdaysWords.length"
    />
  </ModalWindow>
  <ModalWindow
   v-if="showLoadModal"
   @toggleVisible="toggleLoadModal"
  >
    <LoginHandler
    :userLoggedIn="userLoggedIn"
    :userId="userId"
    :loginMessage="loginMessage"
    @login="loginUser($event)"
    />
  </ModalWindow>
</template>

<script>
import SpellingBee from './components/SpellingBee.vue'
import WordList from './components/WordList.vue'
import ScoreBar from './components/ScoreBar.vue'
import ModalWindow from './components/ModalWindow.vue'
import LoginHandler from './components/LoginHandler.vue'

function sendRequest(body, dest = '/api') {
    return fetch(dest, {
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
    ScoreBar,
    ModalWindow,
    LoginHandler
  },
  data() {
    return {
      'showLoadModal': true,
      'loginMessage': 'Please log in or create an account:',
      'userLoggedIn': false,
      'userId': '',
      'showWordModal': false,
      'letters': ['','','','','',''],
      'thresholds': ['Beginner', 'Starting'],
      'scoreLevels': [0, 10],
      'numWords': 1,
      'shuffling': false,
      'required': '',
      'score': 0,
      'previousWords': [],
      'message': '',
      'clearWord': false,
      'yesterdaysWords': []
    }
  },
  created() {
    this.getSetup();
  },
  methods: {
    getSetup() {
      sendRequest({'action': 'get_setup'})
        .then(request => request.json()
          .then(data => {
            if (data.auth) {
              this.userLoggedIn = true;
              this.userId = data.user_id;
              this.letters = data.letters;
              this.thresholds = data.thresholds;
              this.scoreLevels = data.score_levels;
              this.numWords = data.num_words;
              this.required = data.required;
              this.score = data.score;
              this.previousWords = data.already_guessed;
              this.yesterdaysWords = data.yesterday_words;
            }
          })
        )
    },
    loginUser(loginInfo) {
      let requestBody = {
        'action': loginInfo.createNewUser ? 'create_user' : 'login',
        'user_id': loginInfo.userId,
        'secret_word': loginInfo.secretWord
      }
      sendRequest(requestBody, '/login')
      .then(request => request.json()
        .then(data => {
          if (data.success) {
            this.loginMessage = 'Login successful!';
            if (data.secret_word) {
              this.loginMessage = this.loginMessage + `\nYour secret word is: ${data.secret_word}. Write it down for future logins!`
            }
            window.setTimeout(() => {
              this.showLoadModal = false;
            }, 1000);
            this.getSetup();
          } else if (data.reason === 'no user') {
            this.loginMessage = 'No such user.';
          } else if (data.reason === 'bad password') {
            this.loginMessage = 'Wrong secret word.';
          } else if (data.reason === 'user exists') {
            this.loginMessage = 'User already exists';
          } else {
            this.loginMessage = 'Unknown error. Please contact Rich.';
          }
        })
      );
    },
    toggleLoadModal() {
      if (this.userLoggedIn) {
        this.showLoadModal = !this.showLoadModal;
      }
    },
    toggleYesterdayWordModal() {
      this.showWordModal = !this.showWordModal;
    },
    showMessage(message) {
      this.message = '';
      this.message = message;
      this.clearWord = true;
      window.setTimeout(() => {
        this.clearWord = false;
      }, 100);
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

      if (word.join('').toLocaleUpperCase() === 'TACOBELL') {
        this.showMessage(';)');
        return false;
      }

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
            if (data.score === word.length + 7) {
              this.showMessage(`Pangram! +${data.score - 7} +7`)
            } else {
              let scoreMessages = [
                '', 'Nice!', '', '', '',
                'Great!',
                'Awesome!',
                'Wow!',
                'Stupendous!',
                'Incredible!'
              ]

              this.showMessage(`${scoreMessages[data.score] || 'Incredible!'} +${data.score}`)
            }
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
  display: flex;
  flex-direction: row;
  justify-content: center;
  margin: 0;
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
  width: 100vw;
  padding: 0;
  max-width: 1200px;
  padding: 0 20px;
  overflow-x: hidden;
}


#title {
  grid-area: title;
  border-bottom: 3px solid #2f2f2f;
  padding-bottom: 20px;
  margin-bottom: 0;
}


#yesterday-modal {
  position: fixed;
  top: 10px;
  right: 10px;
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

  #title {
    min-height: 75px;
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: center;
    padding-bottom: 0;
  }

  #title > h1 {
    font-size: 16pt;
    max-width: 150px;
  }

  
  #yesterday-modal {
    position: unset;
  }
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

.no-overflow {
  overflow-y: hidden
}

</style>
