<template>
    <div id="spend">
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label for="monthYear">Your spending:</label>
                <select v-model="selectedSpending" class="form-control" id="spendings">
                    <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
                </option>
                </select>
            </div>
        </div>
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label for="years">Year:</label>
                <select v-model="selectedYear" class="form-control" id="years">
                    <option v-for="item in 10">{{yyyy-1 + item}}</option>
                </select>
            </div>
        </div>
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label for="monthYear">Month:</label>
                <select v-model="selectedMonth" class="form-control" id="monthYear">
                    <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }} </option>
                </select>
            </div>
        </div>
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label for="value">Value:</label>
                <br>
                <input v-model.number="selectedValueQ"  id="value"
                    type="number" min="0" max="999999999"
                    placeholder="Your limit" pattern="^\d+(\.\d+)?$">
            </div>
            <hr>
            <div  v-show="isValidData">
                <button v-on:click="setLimit" :variant="secondary" class="btn btn-secondary">Set limit</button>
                <br>
                <button v-on:click="createDone" :variant="secondary" v-show="isDone"class="btn btn-secondary">
                    {{msg}}
                </button>
            </div>
        </div>
    </div>
</template>


<script>
import axios from 'axios';

var today = new Date();
var yyyy = today.getFullYear();
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
            isDone: false,
            msg: '',
            spending_list: [],
            yyyy: yyyy,
            selectedYear: null,
            selectedMonth: null,
            selectedValue: null,
            selectedSpending: null,
            errors: [],
            newLimitation: {
                'spending_id': null,
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
        axios({
            method: 'get',
            url: '/api/v1/spending/'
        })
        .then(response => {
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
                url: '/api/v1/spending/set_limit/',
                data: {
                    'spending_id': this.selectedSpending,
                    'year': this.selectedYear,
                    'month': this.selectedMonth,
                    'value': this.selectedValueQ
                }
            }).then(response =>(this.msg = response.data));
                this.isDone=true;
        },
        createDone: function (event) {
            this.$router.go('/spend')
        },
    }
}
</script>

<style scoped>

</style>
