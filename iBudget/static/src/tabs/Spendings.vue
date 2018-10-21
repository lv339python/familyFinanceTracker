<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../spending_registration">Spending Registration</b-button>
            <b-button :variant="secondary" to="../spend">Set individual limitation</b-button>
            <b-button :variant="secondary" to="/limit">Set group limitation</b-button>
            <b-button :variant="secondary" to="/spending_add">Add spending</b-button>
            <b-button :variant="secondary" to="/spending_history">Spending history</b-button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Spendings"
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
