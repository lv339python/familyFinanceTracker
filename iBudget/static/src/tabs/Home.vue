<template>
    <div class="content">
        <div class="text">
            <h1>There will be some thumbnails</h1>
            <h1>and</h1>
            <h1>general information...</h1>
        </div>
    </div>
</template>

<script>

    export default {
        name: "Home",
    }
</script>

<style scoped>
    .content {
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
        text-align: center;
    }

    p {
        width: 400px;
    }
</style>

