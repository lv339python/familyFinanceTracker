<template>
  <div class="content">
      <div class="text">
      <b-button :variant="secondary" to="../funds_registration">Create new fund</b-button>
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
        height: 100vh;
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
