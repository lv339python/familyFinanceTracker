<template>
  <div class="container pt-5" id="spending_registration">
  <div class="row mb-3">
    <div class="col-md-4">
      <h1>Spending history</h1>
    </div>
    <div class="row">
      <div class="col-md-12 pt-2">
        <div>
          <label >Select category:</label>

            <select v-model="category" class="ourform">
              <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
              </option>
            </select>

          <label>Chose type_of_pay:</label>

            <select v-model="type_of_pay" class="ourform">
              <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id"> {{ type_of_pay.name }}
              </option>
            </select>
          <label>Input sum</label>
          <input v-model="sum" type="number" class="date">

          <label>Comment</label>
          <input v-model="comment" type="text">
          <div>{{ comment }}</div>

          <label>Chose date</label>
          <input v-model="date" type="date">
          <div>{{ date }}</div>

          <button>Shared</button>
          <button v-on:click="setData">Save</button>
          <button>Cancel</button>

        </div>
        <hr>
      </div>

    </div>
  </div>
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
            sum: null,
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
                  'sum': this.sum,
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
