<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../spending_registration">Spending Registration</b-button>
            <b-button :variant="secondary" to="../spend">Set Individual Limitation</b-button>
            <b-button :variant="secondary" to="/limit">Set Group Limitation</b-button>
            <b-button :variant="secondary" to="/spending_add">Add Spending</b-button>
            <b-button :variant="secondary" to="/spending_history">Spending History</b-button>
        </div>
    </div>
</template>

<script>
    export default {
        name: "Spendings",
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
