<template>
  <div class="content">
      <div class="text">
      <b-button :variant="secondary" to="../Financial_goal">Financial goal</b-button>
      <b-button :variant="secondary" to="../funds_registration">Create new fund</b-button>
        <b-button :variant="secondary" to="/goal">Goal</b-button>
          <b-button :variant="secondary" to="/goaltable">Goal Table</b-button>
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
