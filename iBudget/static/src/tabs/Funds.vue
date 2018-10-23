<template>
  <div class="content">
      <div class="text">
      <b-button :variant="secondary" to="../Financial_goal">Financial goal</b-button>
      <b-button :variant="secondary" to="../funds_registration">Create new fund</b-button>
        <b-button :variant="secondary" to="/goal">GOAL</b-button>
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
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
