<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/spendings/add">Add</b-button>
            <b-button :variant="secondary" to="/spendings/limit_ind">Set Individual Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/limit_group">Set Group Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/history">History</b-button>
            <b-button :variant="secondary" to="/spendings/new">New</b-button>
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
        width: 16%;
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
