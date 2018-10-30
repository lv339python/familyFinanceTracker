<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/spendings/spending_registration">Spending Registration</b-button>
            <b-button :variant="secondary" to="/spendings/spend">Set Individual Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/limit">Set Group Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/spending_add">Add Spending</b-button>
            <b-button :variant="secondary" to="/spendings/spending_history">Spending History</b-button>
        </div>
        <div  id="right" class="column">
              <router-view></router-view>
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
        height: 100%;
        overflow: hidden;
        margin: 0px;
        display: flex;
    }
    .column {
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    #left {
        flex-shrink: 0;
        background-color: whitesmoke;
        margin: 5px;
        padding: 5px;
    }
    #right {
        background-color: #f3f3f3;
        padding: 5px;
        margin: 0;
        width: 100%;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
