<template>
    <div id="spend">
        <div class="col-md-4">

          <div class="form-group">
            <label for="monthYear">Your spending:</label>
            <hr>
            <select v-model="selectedSpending" class="form-control" id="spendings">
              <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
              </option>
            </select>
           </div>
           <div>  Selected: {{ selectedSpending}} </div>
        </div>

    <div class="col-md-4">
        <div class="form-group">
        <label for="years">Year:</label>
          <hr>
        <select v-model="selectedYear" class="form-control" id="years">
          <option>2018</option>
          <option>2019</option>
          <option>2020</option>
          <option>2021</option>
          <option>2022</option>
          <option>2023</option>
          <option>2024</option>
          <option>2025</option>
          <option>2026</option>
          <option>2027</option>
        </select>
        </div>
        <div>  Selected: {{ selectedYear }} </div>
      </div>

      <div class="col-md-4">
        <div class="form-group">
          <hr>
        <label for="monthYear">Month:</label>
          <select v-model="selectedMonth" class="form-control" id="monthYear">
              <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }} </option>
          </select>
        </div>
        <div>  Selected: {{ selectedMonth}} </div>
      </div>
         <div class="col-md-4">
        <div class="form-group">
          <hr>
        <label for="value">Value:</label>
          <input v-model.number="selectedValueQ"  id="value" type="number" min="0" max="999999999"
                 placeholder="Your limit" pattern="^\d+(\.\d+)?$">
        </div>

        <hr>
        <div  v-show="isValidData">
          <button v-on:click="setLimit" class="btn btn-primary ml-5">Set limit</button>
        </div>

      </div>
    </div>
</template>

<script>
import axios from 'axios';
    export default {
     name: "Spend",
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
      spending_list: [],

       selectedYear: null,
       selectedMonth: null,
       selectedValue: null,
       selectedSpending: null,
       errors: [],
       newLimitation: {
        "spending_id": null,
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
                         this.selectedSpending !=null &&
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
    axios.get('/spending/')
    .then(response => {
      // JSON responses are automatically parsed.
      this.spending_list = response.data
    })
    .catch(e => {
      this.errors.push(e)
    })
  },

  methods: {
    setLimit: function (event) {
      axios({
              method: 'post',
              url: '/spending/set_limit/',
              data: {
                  'spending_id': this.selectedSpending,
                  'year': this.selectedYear,
                  'month': this.selectedMonth,
                  'value': this.selectedValueQ
                }
             }).then(response =>{
                this.$router.go('/spending/set_limit')
             })
    }
  }
}
</script>

<style scoped>

</style>
