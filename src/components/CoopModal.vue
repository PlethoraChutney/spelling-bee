<template>
    <div class="modal-container">
        <h2>Work together!</h2>
        <p>
            Want to help your friends? Enter their username here to see
            what words you have that they don't.
        </p>
        <p>
            Give good hints, don't just tell them the words!
        </p>
        <div class="h-flex">
            <input type="text" v-model="this.coopUser">
            <div
            class="button"
            @click="$emit('getCoopWords', coopUser)"
            >Get words</div>
        </div>
        <div class="h-flex" id="friends-container">
            <p>Friends:</p>
            <div class="button"
            style="padding: 10px;"
            v-for="(friend, index) in friendList"
            :key="index"
            :class="{'current-friend': friend === this.coopUser}"
            @click="this.coopUser = friend; $emit('getCoopWords', friend)"
            @contextmenu.prevent="$emit('removeFriend', friend)"
            >
            {{friend}}
            </div>
        </div>
        <div
        v-if="!coopUserSuccess">
            <p>
                I couldn't find that user --- check spelling and capitalization!
            </p>
        </div>
    </div>

    <WordList
    v-if="coopWords.length !== 0"
    :wordList="coopWords"
    :numWords="coopWords.length"
    :foundWords="[]"
    />
    <p v-if="hasCooperated && coopWords.length === 0 && coopUserSuccess">
        Looks like they've got all your words!
    </p>
</template>

<script>
import WordList from './WordList.vue'

export default {
    components: {WordList},
    props: {
        'coopWords': Array,
        'coopUserSuccess': Boolean,
        'hasCooperated': Boolean,
        'friendList': Array
    },
    emits: ['getCoopWords', 'removeFriend'],
    data() {
        return {
            'coopUser': ''
        }
    }
}
</script>

<style scoped>

input {
    height: 1.5rem;
    box-sizing: border-box;
    border: 1px solid #e2e2e2;
    margin: 5px;
}

input:focus {
    outline: none;
    border: 2px solid #f7da21;
}

div.h-flex {
    display: flex;
    flex-direction: row;
    justify-content: center;
    align-items: center;
}

div#friends-container {
    flex-wrap: wrap;
}

div.modal-container {
    width: 90%;
    margin: 10px;
}

div.button.current-friend {
    background-color: #f7da21;
}

</style>