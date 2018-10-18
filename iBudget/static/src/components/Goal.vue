<template>
  <div class="content" id="goal">
      <div class="text">

      <ul>
        <il v-for="goal in user_goal_list"> {{ goal.name}} - {{ goal.value }}-{{goal.transaction}} </il>
        </ul>
        <chart1> </chart1>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
    export default {
        name: "Goal",
        data() {
          return{
            user_goal_list: [],
            start_date: null,
            finish_date: null,
            value: null,
            transaction: [],
            name: null,
            is_active: true
           }
        },
        created(){
          axios.get('api/v1/fund/show_goal_data/')
            .then(response => {
            // JSON responses are automatically parsed.
            this.user_goal_list = response.data
          })
          .catch(e => {
          this.errors.push(e)
          })
        }
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
