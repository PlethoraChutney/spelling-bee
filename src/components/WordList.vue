<script>
export default {
    props: {
        'wordList': Array
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
            let thirdsIndex = Math.floor(this.wordList.length / 3)
            return [
                this.titleCaseWordList.slice(0, thirdsIndex),
                this.titleCaseWordList.slice(thirdsIndex, thirdsIndex*2),
                this.titleCaseWordList.slice(thirdsIndex*2)
            ];
        }
    }
}
</script>

<template>
    <div id="word-columns">
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[0]"
            :key="index">
                {{word}}
            </p>
        </div>
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[1]"
            :key="index">
                {{word}}
            </p>
        </div>
        <div class="column">
            <p
            v-for="(word, index) in thirdSplit[2]"
            :key="index">
                {{word}}
            </p>
        </div>
    </div>
</template>

<style scoped>
#word-columns {
    overflow-y: scroll;
    scrollbar-width: none;
    max-height: 500px;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
    margin-top: 20px;
    text-align: left;
}
.column {
    display: flex;
    flex-direction: column;
    justify-content: center;
}
p {
    margin-top: 0;
    margin-bottom: 1rem;
}

</style>