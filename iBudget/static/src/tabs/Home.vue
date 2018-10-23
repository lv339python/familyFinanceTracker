<template>
  <div class="content">
      <div class="text">

    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Chart1  from 'src/components/examples/Chart1';
    export default {
        name: "Home",
    }
</script>

<style scoped>
  .content{
    overflow: hidden;
    display: flex;
  }
  .text{
    width: fit-content;
    margin:  auto;
    text-align: center;
  }
  p{
    width: 400px;
  }
</style>

