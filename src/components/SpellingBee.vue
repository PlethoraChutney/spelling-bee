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
    <div id="letter-swarm">
        <LetterHex
        :key="`required_letter`"
        :letter="required"
        :position="`position-required`"
        :isRequired="true"/>

        <LetterHex
        v-for="(letter, index) in letters"
        :key="index"
        :letter="letter"
        :position="`position-` + String(index)"
        :isRequired="false"/>
    </div>
    
</template>

<style>
div#letter-swarm {
    width: 300px;
    height: 300px;
    position: relative;
}

#letter-swarm > svg {
    position: absolute;
}

#letter-swarm > .position-required {
    top: 100px;
    left: 100px;
}

#letter-swarm > .position-0 {
    bottom: 200px;
    left: 100px;
}

#letter-swarm > .position-1 {
    bottom: 150px;
    left: 13.39px;
}

#letter-swarm > .position-2 {
    bottom: 50px;
    left: 13.39px;
}

#letter-swarm > .position-3 {
    bottom: 0px;
    left: 100px;
}

#letter-swarm > .position-4 {
    bottom: 50px;
    left: 186.6px;
}

#letter-swarm > .position-5 {
    bottom: 150px;
    left: 186.6px;
}


</style>