<script>
let points = [];
[0, 1/3, 2/3, 1, 4/3, 5/3, 2].forEach(e => {
                points.push([50*(Math.cos(Math.PI * e)+1), 50*(Math.sin(Math.PI * e)+1)])
            });

export default {
    props: {
        'letter': String,
        'isRequired': Boolean,
        'position': String
    },
    data() {
        return {
            'points': points
        }
    }
}
</script>

<template>
    <svg width="100" height="100" :class="position">
        <polygon
        :points="points"
        :class="{'required': isRequired}"
        />
        <text
        x="50%" y="50%"
        text-anchor="middle"
        dominant-baseline="middle">{{letter.toLocaleUpperCase()}}</text>
    </svg>
</template>

<style scoped>
polygon {
    fill: #e6e6e6;
}

polygon.required {
    fill: #f7da21;
}

svg:hover {
    filter: brightness(0.9);
}

text {
    font-size: 20pt;
    font-weight: bold;
    user-select: none;
}
</style>