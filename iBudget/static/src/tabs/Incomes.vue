<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="/incomes/add">Add</b-button>
            <b-button :variant="secondary" to="/incomes/tracking">Tracking</b-button>
            <b-button :variant="secondary" to="/incomes/new">New</b-button>
        </div>
    </div>

</template>

<script>
    export default {
        name: "Incomes"
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
    }
</style>
