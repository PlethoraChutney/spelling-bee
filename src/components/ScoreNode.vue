<script>
export default {
    props: {
        'currentScore': Number,
        'nodeThreshold': Number,
        'xPosition': Number,
        'isActive': Boolean
    }
}
</script>

<template>
    <circle
    v-if="!isActive"
    :cx="xPosition"
    cy="25"
    :class="{'completed': currentScore >= nodeThreshold}"
    r="5"
    />
    <circle
    v-else
    :cx="xPosition"
    cy="25"
    class="current-node completed"
    r="15"
    />
    <text
    v-if="isActive"
    :x="xPosition"
    y="26"
    text-anchor="middle"
    dominant-baseline="middle"
    >{{currentScore}}</text>
</template>

<style scoped>
circle {
    fill: #e6e6e6;
}

circle.completed {
    fill: #f7da21;
}

circle.current-node {
    z-index: 1;
}

text {
    font-size: 10pt;
    user-select: none;
}
</style>