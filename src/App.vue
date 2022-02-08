<template>
  <SpellingBee :letters="letters" :required="required"/>
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

export default {
  name: 'App',
  components: {
    SpellingBee
  },
  data() {
    return {
      'letters': ['','','','','',''],
      'required': ''
    }
  },
  created() {
    document.title = 'Spelling Bee';

    sendRequest({'action': 'get_setup'})
      .then(request => request.json()
        .then(data => {
          this.letters = data.letters;
          this.required = data.required
        })
      )
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
