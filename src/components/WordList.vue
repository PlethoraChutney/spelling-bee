<script>
export default {
    props: {
        'wordList': Array,
        'foundWords': Array,
        'numWords': Number
    },
    computed: {
        titleCaseWordList() {
            let titleWords = [];
            this.wordList.forEach(word => {
                let wordArray = word.split('');
                wordArray[0] = wordArray[0].toLocaleUpperCase();
                titleWords.push(wordArray.join(''))
            });

            titleWords.sort(function(a, b) {
                return a.length - b.length || a.localeCompare(b)
            })
            return titleWords;
        },
        thirdSplit() {
            let split = Math.round(this.numWords/3) + 1;
            return [
                this.titleCaseWordList.slice(0, split),
                this.titleCaseWordList.slice(split, split*2),
                this.titleCaseWordList.slice(split*2)
            ];
        }
    },
    methods: {
        getUniqueChars(str) {
            return String.prototype.concat(...new Set(str)).length;
        }
    }
}
</script>

<template>
    <div id="word-columns">
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[0]"
            :key="index"
            :class="{
                'found': foundWords.includes(word.toLocaleLowerCase()),
                'pangram': this.getUniqueChars(word) === 7}">
                {{word}}
            </p>
        </div>
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[1]"
            :key="index"
            :class="{
                'found': foundWords.includes(word.toLocaleLowerCase()),
                'pangram': this.getUniqueChars(word) === 7}">
                {{word}}
            </p>
        </div>
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[2]"
            :key="index"
            :class="{
                'found': foundWords.includes(word.toLocaleLowerCase()),
                'pangram': this.getUniqueChars(word) === 7}">
                {{word}}
            </p>
        </div>
    </div>
</template>

<style scoped>
#word-columns {
    overflow-y: scroll;
    scrollbar-width: none;
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
    text-align: left;
    border: 3px solid #dddddd;
    border-radius: 5px;
    width: 100%;
    max-width: 90%;
    min-height: 50vh;
    max-height: 70vh;
}
.column {
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    width: 25%;
    margin-left: 2.5%;
    margin-right: 2.5%;
}
p {
    margin-top: 0.5rem;
    margin-bottom: 0.5rem;
    width: 100%;
    border-bottom: 1px solid #dddddd;
}

p.found {
    text-decoration: line-through;
    color: #aaa;
}

p.pangram {
    color: #f7da21;
    animation: glow 3s infinite;
    font-weight: bold;
}

@keyframes glow {
    0%   {filter: brightness(0.9);}
    50%  {filter: brightness(1.1);}
    100% {filter: brightness(0.9);}
}

</style>
