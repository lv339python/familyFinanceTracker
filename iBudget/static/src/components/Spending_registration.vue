<template>
    <div id="spending_registration">
        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label >Select category:</label>
            <select v-model="category" class="form-control">
              <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
              </option>
            </select>
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Choose type of pay:</label>
            <select v-model="type_of_pay" class="form-control">
              <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id"> {{ type_of_pay.name }}
              </option>
            </select>
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input sum</label>
            <input v-model="value" type="number" min="1" class="form-control">
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input comment</label>
            <input v-model="comment" type="text" class="form-control">
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Choose date</label>
            <input v-model="date" type="date">
           </div>
           <hr>
        </div>

        <button v-on:click="setData" :variant="secondary">Save</button>
        <button :variant="secondary">Shared</button>
    </div>
</template>

<script>
import axios from 'axios';
    export default {
        name: "spending_history",
        data() {
          return{
            spending_list: [],
            fund_list: [],
            category: null,
            type_of_pay: null,
            value: null,
            date:null,
            comment:null,

           }
        },

        created(){
          axios.get('/api/v1/spending/')
            .then(response => {
            // JSON responses are automatically parsed.
            this.spending_list = response.data
          })
          .catch(e => {
          this.errors.push(e)
          })
          axios.get('/api/v1/fund/')
            .then(response => {
            // JSON responses are automatically parsed.
            this.fund_list = response.data
          })
          .catch(e => {
          this.errors.push(e)
          })
        },
        methods: {

          setData: function (event) {
            axios({
              method: 'post',
              url: '/api/v1/spending_history/register_spending/',
              data: {
                  'category': this.category,
                  'type_of_pay': this.type_of_pay,
                  'date': this.date,
                  'value': this.value,
                  'comment': this.comment,
                }
             }).then(response =>{
                this.$router.go('/Spendings/')
             })
          }
  }
}
</script>

<style scoped>
.content{
  height: 100vh;
  overflow: hidden;
  display: flex;
}
  .text{
    width: fit-content;
    margin:  auto;
  }
</style>
