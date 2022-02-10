<script>
export default {
    props: {
        'score': Number,
        'thresholds': Array,
        'scoreLevels': Array
    },
    computed: {
        currentScoreLevel() {
            var currentThreshold = null;
            for (let i = 0; i < this.scoreLevels.length - 1; i++) {
                if (this.score >= this.scoreLevels[i] && this.score < this.scoreLevels[i+1]) {
                    currentThreshold = this.thresholds[i];
                }
            }

            if (currentThreshold == null) {
                currentThreshold = this.thresholds[this.thresholds.length - 1];
            }

            return currentThreshold;
        }
    }
}
</script>

<template>
    <p>{{currentScoreLevel}}</p>
</template>

<style scoped>

</style>