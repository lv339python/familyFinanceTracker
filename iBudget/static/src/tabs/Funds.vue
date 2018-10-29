<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="/funds/tracking_goal">Tracking Goal</b-button>
            <b-button :variant="secondary" to="/funds/new_goal">New Goal</b-button>
            <b-button :variant="secondary" to="/funds/new">New Fund</b-button>

        </div>
    </div>

</template>

<script>
    export default {
        name: "Funds"
    }
</script>

<style scoped>
    .content {
        overflow: scroll;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
