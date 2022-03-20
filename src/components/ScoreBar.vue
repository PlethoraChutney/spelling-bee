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
        currentScoreEmoji() {
            let emoji = '👶'
            switch (this.currentScoreLevel) {
                case 'Beginner':
                    emoji = '👶'
                    break;
                case 'Good Start':
                    emoji = '✏️'
                    break;
                case 'Moving Up':
                    emoji = '↗️'
                    break;
                case 'Good':
                    emoji = '👍'
                    break;
                case 'Solid':
                    emoji = '⛰️'
                    break;
                case 'Nice':
                    emoji = '😎'
                    break;
                case 'Great':
                    emoji = '👏'
                    break;
                case 'Amazing':
                    emoji = '😮'
                    break;
                case 'Genius':
                    emoji = '🧠'
                    break;
                case 'Queen Bee':
                    emoji = '👑🐝'
                    break;
                default:
                    break;
            }
            return emoji;
        },
        scoreSvgPaths() {
            let currentPercentScore = this.score/this.scoreLevels[this.scoreLevels.length - 1] * 350 + 15;
            return [
                `M 15 25 l ${currentPercentScore} 0`,
                `M ${currentPercentScore} 25 L 365 25`
            ]
        },
        currentNonCurrentSplit() {
            // Need this becasue SVG z-indexing is purely determined by when an element is built
            var nonCurrentScoreLevels = [];
            var currentScoreLevel = [];
            this.thresholds.forEach((threshold, index) => {
                if (threshold !== this.currentScoreLevel) {
                    nonCurrentScoreLevels.push([this.scoreLevels[index], threshold]);
                } else {
                    currentScoreLevel.push([this.scoreLevels[index], threshold]);
                }
            })

            return {'nonCurrent': nonCurrentScoreLevels, 'current': currentScoreLevel};
        },
        emojiString() {
            let currentEmojiString = [`${this.score} · ${this.currentScoreLevel} ${this.currentScoreEmoji}`];
            if (this.currentScoreLevel !== 'Queen Bee') {
                currentEmojiString.push(':\n');
                this.scoreLevels.forEach(scoreLevel => {
                    if (scoreLevel <= this.score) {
                        currentEmojiString.push('🟡');
                    } else {
                        currentEmojiString.push('⚪');
                    }
                })
            }
            return currentEmojiString.join('');
        }
    },
    methods: {
        copyToClipboard() {
            navigator.clipboard.writeText(this.emojiString);
            this.$emit('emojiStringCopied');
        }
    }
}
</script>

<template>
    <div id="score-bar">
        <p class="v-center">{{currentScoreLevel}}</p>
        <svg
        width="380"
        height="50"
        @click="copyToClipboard()"
        >
            <path class="current-score" fill="transparent"
            :d="scoreSvgPaths[0]"
            />
            <path class="remaining-score" fill="transparent"
            :d="scoreSvgPaths[1]"
            />
            <ScoreNode
            v-for="(scoreLevel, index) in currentNonCurrentSplit.nonCurrent"
            :key="index"
            :xPosition="scoreLevel[0]/scoreLevels[scoreLevels.length -1] * 350 + 15"
            :nodeThreshold="scoreLevel[0]"
            :currentScore="score"
            :isActive="currentScoreLevel === scoreLevel[1]"
            />
            <ScoreNode
            v-for="(scoreLevel, index) in currentNonCurrentSplit.current"
            :key="index"
            :xPosition="scoreLevel[0]/scoreLevels[scoreLevels.length -1] * 350 + 15"
            :nodeThreshold="scoreLevel[0]"
            :currentScore="score"
            :isActive="currentScoreLevel === scoreLevel[1]"
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
    align-items: center;
}

@media screen and (max-width: 650px) {
  #score-bar {
    flex-direction: column;
  }
}

p {
    width: 80px;
    white-space: pre-wrap;
    height: 50px;
    font-weight: bold;
    margin: 0;
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
