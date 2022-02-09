<script>
import LetterHex from './LetterHex.vue'

export default {
    name: 'SpellingBee',
    components: {LetterHex},
    props: {
        'letters': Array,
        'required': String
    }
}
</script>

<template>
    <h1>Lindsey's Spelling Bee</h1>
    <svg id="letter-swarm" width="300" height="300">
        <LetterHex
        :key="`required_letter`"
        :letter="required"
        :radius=0
        :angle=0
        :size=50
        :isRequired="true"/>

        <LetterHex
        v-for="(letter, index) in letters"
        :key="index"
        :letter="letter"
        :radius=97
        :angle="index"
        :size=50
        :isRequired="false"/>
    </svg>
    
</template>

<style>

</style>