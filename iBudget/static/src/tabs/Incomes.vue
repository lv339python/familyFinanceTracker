<template>
    <div class="content">

        <income_tracker/>
    </div>

</template>

<script>
     import Income_tracker from 'src/components/Income_tracker';

    export default {
        name: "Incomes",
        components: {
            'Income_tracker': Income_tracker}
    }
</script>

<style scoped>
    .content {
        height: 100%;
        overflow: hidden;
        display: flex;
    }
    .text {
        width: fit-content;
        margin: auto;
    }
</style>
