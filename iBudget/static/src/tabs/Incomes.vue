<template>
  <div class="content">
      <div class="text">
          <h1>There will be incomes...</h1>
          <b-button :variant="secondary" to="../income_registration">Income Registration</b-button>
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
