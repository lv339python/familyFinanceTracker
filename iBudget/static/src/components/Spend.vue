<template>
    <div id="spend">
        <div class="col-md-3" v-if="fixed == null" @change="setPeriod()">
            <p>You want to set limits by day or by month/year? Choose below:</p>
            <input type="radio" id="one" value="True" v-model="fixed">
            <label for="one">Monthly/yearly</label>
            <br>
            <input type="radio" id="two" value="False" v-model="fixed">
            <label for="two">Arbitrary</label>
        </div>
        <div class="wrapper" v-if="fixed !== null">
            <div class="form-holder">
                <div>
                <hr>
                <div class="form-group">
                    <label for="monthYear">Your Spending:</label>
                    <select v-model="selectedSpending" class="form-control" id="spendings" required>
                        <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-if="fixed == true | fixed =='True'" class="monthly-form">
                <div>
                    <hr>
                    <div class="form-group">
                        <label for="years">Year:</label>
                        <select v-model="selectedYear" class="form-control" id="years" required>
                            <option v-for="item in 10">{{yyyy-1 + item}}</option>
                        </select>
                    </div>
                </div>
                <div>
                    <hr>
                    <div class="form-group">
                        <label for="monthYear">Month:</label>
                        <select v-model="selectedMonth" class="form-control" id="monthYear" required>
                            <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }}</option>
                        </select>
                    </div>
                </div>
                <div>
                    <hr>
                    <div class="form-group">
                        <label for="value">Value:</label>
                        <br>
                        <input
                            v-model.number="selectedValueQ"
                            id="value"
                            type="number" min="0" max="999999999"
                            placeholder="Your limit" pattern="^\d+(\.\d+)?$" required>
                    </div>
                    <hr>
                    <div>
                        <button v-on:click="setLimitFix"
                            :variant="secondary"
                            class="btn btn-outline-primary"
                            :disabled="isValidDataFix===false">Set Limit
                        </button>
                    </div>
                </div>
            </div>

            <div v-if="fixed==false | fixed=='False'">
                <div class="form-group">
                    <hr>
                    <div>
                        <label>Select Start Date</label>
                        <input v-model="start_date" type="date">
                    </div>
                    <hr>
                </div>
                <div class="form-group">
                    <div>
                        <label>Select Final Date</label>
                        <input v-model="finish_date" type="date">
                        <hr>
                    </div>
                </div>
                <div>

                    <div class="form-group">
                        <label for="value">Value:</label>
                        <br>
                        <input
                            v-model.number="selectedValueQ"
                            id="value"
                            type="number" min="0" max="999999999"
                            placeholder="Your limit" pattern="^\d+(\.\d+)?$" required>
                    </div>
                    <hr>
                    <div>
                        <button v-on:click="setLimitArb"
                            :variant="secondary"
                            class="btn btn-outline-primary"
                            :disabled="isValidDataArb===false">Set Limit
                        </button>
                    </div>
                </div>
            </div>
            </div>

        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    var today = new Date();
    var yyyy = today.getFullYear();
    var UTC = -new Date().getTimezoneOffset() / 60

    export default {
        name: "Spend",
        data() {
            return {
                months: [
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
                msg: '',
                spending_list: [],
                fixed: null,
                yyyy: yyyy,
                selectedYear: null,
                selectedMonth: null,
                selectedValue: null,
                start_date: new Date().toJSON().slice(0,10),
                finish_date: new Date().toJSON().slice(0,10),
                selectedSpending: null,
                errors: [],
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
            isValidDataFix: {
                get: function () {
                    var result =
                        this.selectedSpending != null &&
                        this.selectedYear != null &&
                        this.selectedMonth != null &&
                        typeof(this.selectedValueQ) === 'number' &&
                        this.selectedValueQ > 0 &&
                        this.selectedValueQ < 1000000000000000;
                    return result;
                }
            },
            isValidDataArb: {
                get: function () {
                    var result =
                        this.selectedSpending != null &&
                        this.start_date != null &&
                        this.finish_date != null &&
                        this.start_date <=this.finish_date &&
                        typeof(this.selectedValueQ) === 'number' &&
                        this.selectedValueQ > 0 &&
                        this.selectedValueQ < 1000000000000000;
                    return result;
                }
            },
        },
        created() {
            axios({
                method: 'get',
                url: '/api/v1/spending/'
            })
                .then(response => {
                    this.spending_list = response.data.categories;
                    this.fixed = response.data.fixed;
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setPeriod: function () {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/set_period/',
                    data: {
                        'fixed': this.fixed
                    }
                }).then(response => {
                    this.msg = response.data;
                    alert(this.msg);
                });
                 this.$router.push('/spendings/limit_ind')
            },
            setLimitFix: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/set_limit_fix/',
                    data: {
                        'spending_id': this.selectedSpending,
                        'year': this.selectedYear,
                        'month': this.selectedMonth,
                        'value': this.selectedValueQ
                    }
                }).then(response => {
                    this.msg = response.data;
                    alert(this.msg);
                    this.createDone();
                });
            },
            setLimitArb: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/set_limit_arb/',
                    data: {
                        'spending_id': this.selectedSpending,
                        'start_date': String(this.start_date),
                        'finish_date': String(this.finish_date),
                        'UTC': UTC,
                        'value': this.selectedValueQ
                    }
                }).then(response => {
                    this.msg = response.data;
                    alert(this.msg);
                    this.createDone();
                });
            },
            createDone: function (event) {
                this.isDone = false;
                this.msg = '';
                this.selectedYear = null;
                this.selectedMonth = null;
                this.selectedValue = null;
                this.start_date = new Date().toJSON().slice(0,10);
                this.finish_date =new Date().toJSON().slice(0,10);
                this.selectedSpending = null;
            },
        }
    }
</script>

<style scoped>
    .wrapper{
        display: flex;
    }
    .form-holder{
        margin: auto;
        display: flex;
        flex-direction: column;
        text-align: center;
        width: 25%;
    }

</style>
