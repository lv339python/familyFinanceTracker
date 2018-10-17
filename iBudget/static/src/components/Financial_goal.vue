<template>
    <div id="spend">
       <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose group</label>
            <select v-model="group" class="ourform">
            <option v-for="group in group_list"
                      v-bind:value="group.id"
                      v-on:click="is_active_shared_fund=group.id">
                      {{ group.name }}
            </option>
            </select>
          </div>
          <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose fund</label>
            <select v-model="fund" class="ourform" >
            <option v-for="fund in fund_list"
                      v-if="fund.id_group === is_active_shared_fund"
                      v-bind:value="fund.id_fund">
                      {{fund.name_fund}}
            </option>
            </select>
          </div>
          <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Start date</label>
            <input v-model="start_date" type="date">
           </div>
           <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Finish date</label>
            <input v-model="finish_date" type="date">
           </div>
           <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input value</label>
            <input v-model="value" type="number" min="1" class="form-control">
           </div>
        </div>

        <button v-on:click="setData" :variant="secondary">Save</button>
    </div>
</template>

<script>
import axios from 'axios';
     export default {
     name: "Financial_goal",
     data () {
     return {
       fund_list: [],
       group_list:null,
       fund:null,
       start_date:null,
       finish_date:null,
       value:null,
       is_active_shared_fund:null


    }
  },
   created(){
          axios.get('/api/v1/fund/show_fund_group/')
            .then(response => {
            // JSON responses are automatically parsed.
            this.fund_list = response.data
          })
          .catch(e => {
          this.errors.push(e)
          });
          axios.get('/api/v1/group/get_by_group/')
            .then(response => {
            // JSON responses are automatically parsed.
            this.group_list = response.data;
          })
          .catch(e => {
          this.errors.push(e)
          });
        },
  methods: {
    setData: function (event) {
      axios({
              method: 'post',
              url: '/api/v1/fund/register_financial_goal_group/',
              data: {
                  'value': this.value,
                  'start_date': this.start_date,
                  'finish_date': this.finish_date,
                  'fund': this.fund
                }
             }).then(response =>{
                this.$router.go('fund/register_financial_goal_ind')
             })
    }
  }
}
</script>

<style scoped>

</style>
