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
    class="current-node"
    r="10"
    />
</template>

<style scoped>
circle {
    fill: #e6e6e6;
}

circle.completed, circle.current-node {
    fill: #f7da21;
}
</style>