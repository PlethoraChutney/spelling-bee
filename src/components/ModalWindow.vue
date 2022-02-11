<script>
export default {
    
}
</script>

<template>
    <div id="bounding-box" @click="$emit('toggleVisible')">
        <div id="modal-window" @click.stop>
            <div id="content">
                <slot></slot>
            </div>
        </div>
    </div>
</template>

<style scoped>

div#bounding-box {
    margin: 0;
    padding: 0;
    height: 100%;
    width: 100%;
    background-color: #f7da21;
    z-index: 1;
    position: absolute;
    left: 0;
    top: 0;
}

div#modal-window {
    width: 80%;
    max-height: 80%;
    overflow-y: scroll;
    overflow-x: hidden;
    border-radius: 10px;
    scrollbar-width: none;
    margin: 10vh auto;
    position: relative;
    background-color: white;
}

div#content {
    margin: 0 auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}
</style>