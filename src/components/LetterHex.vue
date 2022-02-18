<script>
let points = [];
[0, 1/3, 2/3, 1, 4/3, 5/3, 2].forEach(e => {
                points.push([(Math.cos(Math.PI * e)), (Math.sin(Math.PI * e))])
            });

export default {
    props: {
        'letter': String,
        'isRequired': Boolean,
        'radius': Number,
        'angle': Number,
        'size': Number,
        'shuffling': Boolean
    },
    computed: {
        hexPoints: function() {
            let scaledPoints = [];
            points.forEach(e => {
                scaledPoints.push(
                    [e[0] * this.size, e[1] * this.size]
                )
            });
            let shiftedPoints = [];
            scaledPoints.forEach(e => {
                shiftedPoints.push(
                    [
                        e[0] + Math.sin(this.angle * Math.PI/3) * this.radius + 150,
                        e[1] + Math.cos(this.angle * Math.PI/3) * this.radius + 150
                    ]
                )
            });

            return shiftedPoints;
        },
        textPoints: function() {
            let centerPoint = [];
            let xPoints = [];
            let yPoints = [];
            const average = arr => arr.reduce((a,b) => a + b, 0) / arr.length;

            this.hexPoints.forEach(e => {
                xPoints.push(e[0]);
                yPoints.push(e[1]);
            })

            centerPoint.push(average(xPoints));
            centerPoint.push(average(yPoints));

            return centerPoint;
        }
    }
}
</script>

<template>
    <g @click="$emit('typeLetter', letter)">
    <polygon
    :points="hexPoints"
    :class="{'required': isRequired}"
    />
    <text
    :x="textPoints[0] - 7"
    :y="textPoints[1] + 5"
    :class="{'hide-for-shuffle': shuffling}"
    text-anchor="middle"
    dominant-baseline="middle">{{letter.toLocaleUpperCase()}}</text>
    </g>
</template>

<style scoped>
polygon {
    fill: #e6e6e6;
    touch-action: none;
}

polygon.required {
    fill: #f7da21;
}

g {
    cursor: pointer;
}

g:hover {
    filter: brightness(0.9);
}

text {
    font-family: Lato, sans-serif;
    font-size: 24pt;
    font-weight: bold;
    user-select: none;
    touch-action: none;
}

text.hide-for-shuffle {
    animation: shuffle-opacity 800ms;
}

@keyframes shuffle-opacity {
    0%   {opactiy: 1}
    50%  {opacity: 0}
    100% {opacity: 1}
}
</style>