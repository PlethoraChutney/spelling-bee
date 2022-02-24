<template>
    <div
    :class="{'has-message': message.length !== 0, 'good-message': message.includes('!')}">{{message}}</div>
</template>

<script>
export default {
    props: {
        'message': String
    }
}
</script>

<style scoped>
div {
    background-color: #2f2f2f;
    color: #f1f1f1;
    font-size: 10pt;
    opacity: 0;
    padding: 20px;
    border-radius: 20px;
    min-height: 1.5rem;
    width: max-content;
    display: flex;
    flex-direction: column;
    justify-content: center;
    position: sticky;
    top: 20px;
}

div.good-message {
    background-color: #f1f1f1;
    color: #2f2f2f;
}

.has-message {
    animation: fade-in-out 1500ms;
}

@keyframes fade-in-out {
    0%   {opacity: 0}
    10%  {opacity: 1}
    90%  {opacity: 1}
    100% {opacity: 0}
}
</style>