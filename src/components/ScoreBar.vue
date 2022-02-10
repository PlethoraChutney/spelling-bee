<script>
import ScoreNode from './ScoreNode.vue'

export default {
    components: {ScoreNode},
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
        },
        scoreSvgPaths() {
            let currentPercentScore = this.score/this.scoreLevels[this.scoreLevels.length - 1] * 350 + 15;
            return [
                `M 15 25 l ${currentPercentScore} 0`,
                `M ${currentPercentScore} 25 L 365 25`
            ]
        }
    }
}
</script>

<template>
    <div id="score-bar">
        <p>{{currentScoreLevel}}</p>
        <svg
        width="380"
        height="50"
        >
            <path class="current-score" fill="transparent"
            :d="scoreSvgPaths[0]"
            />
            <path class="remaining-score" fill="transparent"
            :d="scoreSvgPaths[1]"
            />
            <ScoreNode
            v-for="(scoreLevel, index) in scoreLevels"
            :key="index"
            :xPosition="scoreLevel/scoreLevels[scoreLevels.length -1] * 350 + 15"
            :nodeThreshold="scoreLevel"
            :currentScore="score"
            :isActive="currentScoreLevel === thresholds[index]"
            />
        </svg>
    </div>
</template>

<style scoped>
#score-bar {
    width: 100%;
    display: flex;
    flex-direction: row;
    justify-content: space-around;
}

p {
    width: max-content;
    height: 50px;
}

path {
    stroke-width: 2px;
}

.current-score {
    stroke: #f7da21;
}

.remaining-score {
    stroke: #e6e6e6;
}
</style>