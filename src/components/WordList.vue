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
            return [
                this.titleCaseWordList.slice(0, 20),
                this.titleCaseWordList.slice(20, 40),
                this.titleCaseWordList.slice(40)
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
    display: flex;
    flex-direction: row;
    justify-content: center;
    margin-top: 20px;
    text-align: left;
    border: 3px solid #dddddd;
    border-radius: 5px;
    width: 100%;
    height: 50vh;
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

</style>