<template>
    <div id="spend">
        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Choose type of pay:</label>
            <select v-model="selectedFund" class="form-control">
              <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id"> {{ type_of_pay.name }}
              </option>
            </select>
           </div>
        </div>

    <div class="col-md-4">
        <hr>
        <div class="form-group">
        <label for="years">Year:</label>

        <select v-model="selectedYear" class="form-control" id="years">
          <option v-for="item in 10">{{yyyy-1 + item}}</option>
        </select>
        </div>
      </div>

      <div class="col-md-4">
        <hr>
        <div class="form-group">
        <label for="monthYear">Month:</label>
          <select v-model="selectedMonth" class="form-control" id="monthYear">
              <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }} </option>
          </select>
        </div>
      </div>

      <div class="col-md-4">
        <hr>
        <div class="form-group">
        <label for="value">Value:</label>
          <input v-model.number="selectedValueQ"  id="value" type="number" min="0" max="999999999"
                 placeholder="Your limit" pattern="^\d+(\.\d+)?$">
        </div>

        <hr>
        <div  v-show="isValidData">
        <button v-on:click="setLimit" :variant="secondary" >goal</button>
        </div>

      </div>
    </div>
</template>

<script>
import axios from 'axios';
    var today = new Date();
    var yyyy = today.getFullYear();
    export default {
     name: "Financial_goal",
     data () {
    return {
      months : [
        {nameM: 'All the year', valueM: 0},
        {nameM: 'January', valueM: 1},
        {nameM: 'February', valueM: 2},
        {nameM: 'March', valueM: 3},
        {nameM: 'April', valueM: 4},
        {nameM: 'May', valueM: 5},
        {nameM: 'June', valueM: 6},
        {nameM: 'July', valueM: 7},
        {nameM: 'August', valueM: 8},
        {nameM: 'September', valueM: 9},
        {nameM: 'October', valueM: 10},
        {nameM: 'November', valueM: 11},
        {nameM: 'December', valueM: 12}
      ],
      fund_list: [],
       yyyy: yyyy,
       selectedYear: null,
       selectedMonth: null,
       selectedValue: null,
       selectedFund: null,
       errors: [],
       newLimitation: {
        "fund": null,
        'year': null,
        'month': null,
        'value': 0
        },

    }
  },
  computed: {
      selectedValueQ: {
        get: function () {
          return this.selectedValue;
        },
        set: function (newValue) {
          this.selectedValue = newValue;
        }
      },
      isValidData: {
          get: function(){
            var result =
                         this.selectedFund !=null &&
                         this.selectedYear!=null &&
                         this.selectedMonth != null &&
                         typeof(this.selectedValueQ)==='number' &&
                         this.selectedValueQ>0&&
                         this.selectedValueQ<1000000000000000;
            return result;
          }
      }
},

  created() {
    axios({
              method: 'get',
              url: '/api/v1/fund/'
             })
    .then(response => {
      // JSON responses are automatically parsed.
      this.fund_list = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  },

  methods: {
    setLimit: function (event) {
      axios({
              method: 'post',
              url: '/api/v1/fund/register_financial_goal_ind/',
              data: {
                  'fund_id': this.selectedFund,
                  'year': this.selectedYear,
                  'month': this.selectedMonth,
                  'value': this.selectedValueQ
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
