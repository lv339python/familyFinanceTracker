<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="/spendings/add">Add</b-button>
            <b-button :variant="secondary" to="/spendings/limit_ind">Set Individual Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/limit_group">Set Group Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/history">History</b-button>
            <b-button :variant="secondary" to="/spendings/new">New</b-button>
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
