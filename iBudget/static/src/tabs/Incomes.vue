<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../income_registration">Income Registration</b-button>
            <b-button :variant="secondary" to="/track_incomes">Track Your Incomes</b-button>
            <b-button :variant="secondary" to="/income_add">Add Income Category</b-button>
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
