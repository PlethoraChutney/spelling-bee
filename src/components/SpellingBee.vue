<script>
import LetterHex from './LetterHex.vue'
import WordHolder from './WordHolder.vue'

export default {
    name: 'SpellingBee',
    components: {LetterHex, WordHolder},
    data() {
        return {
            'currentWord': []
        }
    },
    props: {
        'letters': Array,
        'required': String
    },
    emits: ['shuffle-letters'],
    methods: {
        typeLetter(letter) {
            if (letter.length === 1 && letter.match(/[a-z]/i)) {
                let hive = 'out';
                if (letter === this.required) {
                    hive = 'queen';
                } else if (this.letters.includes(letter)) {
                    hive = 'drone';
                }
                this.currentWord.push({
                    'letter': letter.toLocaleUpperCase(),
                    'hive': hive
                });
            } else if (letter.toLocaleUpperCase() === 'ENTER') {
                console.log('Submit word');
            } else if (letter.toLocaleUpperCase() === 'BACKSPACE') {
                this.currentWord.pop();
            } else if (letter.toLocaleUpperCase() === ' ') {
                this.$emit('shuffle-letters');
            }
        }
    },
    mounted() {
        window.addEventListener('keydown', function(e) {
            this.typeLetter(e.key);
        }.bind(this));
    }
}
</script>

<template>
    <h1>Lindsey's Spelling Bee</h1>
    <WordHolder
    :word="currentWord"/>
    <svg id="letter-swarm" width="300" height="300">
        <LetterHex
        @type-letter="typeLetter($event)"
        :key="`required_letter`"
        :letter="required"
        :radius=0
        :angle=0
        :size=50
        :isRequired="true"/>

        <LetterHex
        @type-letter="typeLetter($event)"
        v-for="(letter, index) in letters"
        :key="index"
        :letter="letter"
        :radius=97
        :angle="index"
        :size=50
        :isRequired="false"/>
    </svg>
    <div id="button-container">
        <div
        class="button"
        @click="typeLetter('BACKSPACE')"
        >Delete</div>
        <div
        class="button"
        @click="typeLetter(' ')"
        >Shuffle</div>
        <div
        class="button"
        @click="typeLetter('ENTER')"
        >Enter</div>
    </div>
    
</template>

<style>
.button {
    border: 1px solid #f1f1f1;
    border-radius: 20px;
    padding: 15px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    cursor: pointer;
    user-select: none;
}
#button-container {
    margin-top: 25px;
    width: 300px;
    display: flex;
    justify-content: space-between;
    margin-left: -7px;
}
</style>