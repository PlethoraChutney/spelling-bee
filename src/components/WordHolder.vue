<script>
export default {
    props: {
        'word': Array
    }
}
</script>

<template>
    <div>
        <span
        v-for="(letter, index) in word"
        :key="index"
        :class="letter['hive']"
        >{{letter['letter']}}</span>
        <span class="blinking">|</span>
    </div>    
</template>

<style scoped>
div {
    font-size: 26pt;
    font-weight: bold;
    height: 3rem;
}
span.out {
    color: lightgrey;
}
span.drone {
    color: black;
}
span.queen {
    color: #f7da21;
}
span.blinking {
    animation: 1s blink;
    animation-iteration-count: infinite;
}
@keyframes blink {
    0%   {color: transparent;}
    50%  {color: #f7da21;}
    100% {color: transparent;}
}
</style>