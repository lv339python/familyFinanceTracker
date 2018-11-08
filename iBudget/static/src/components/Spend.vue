<template>
    <div id="spend">
        <div class="col-md-3" v-if="fixed == null" @change="setPeriod()">
            <input type="radio" id="one" value="True" v-model="fixed">
            <label for="one">Monthly/yearly</label>
            <br>
            <input type="radio" id="two" value="False" v-model="fixed">
            <label for="two">Arbitrary</label>
        </div>
        <div v-if="fixed !== null">
            <div class="col-md-4">
                <hr>
                <div class="form-group">
                    <label for="monthYear">Your spending:</label>
                    <select v-model="selectedSpending" class="form-control" id="spendings" required>
                        <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div v-if="fixed == true">
                <div class="col-md-4">
                    <hr>
                    <div class="form-group">
                        <label for="years">Year:</label>
                        <select v-model="selectedYear" class="form-control" id="years" required>
                            <option v-for="item in 10">{{yyyy-1 + item}}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-4">
                    <hr>
                    <div class="form-group">
                        <label for="monthYear">Month:</label>
                        <select v-model="selectedMonth" class="form-control" id="monthYear" required>
                            <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }}</option>
                        </select>
                    </div>
                </div>
                <div class="col-md-4">
                <hr>
                <div class="form-group">
                    <label for="value">Value:</label>
                    <br>
                    <input v-model.number="selectedValueQ" id="value"
                           type="number" min="0" max="999999999"
                           placeholder="Your limit" pattern="^\d+(\.\d+)?$" required>
                </div>
                <hr>
                <div>
                    <button v-on:click="setLimitFix"
                        :variant="secondary"
                        class="btn btn-outline-primary"
                        :disabled="isValidDataFix===false">Set limit
                    </button>
                    <br>
                    <button v-on:click="createDone" :variant="secondary" v-show="isDone" class="btn btn-outline-primary">
                        {{msg}}
                    </button>
                </div>
            </div>

            </div>

            <div v-if="fixed == false ">
                <div class="form-group col-md-4">
                    <div>
                        <label>Select start date</label>
                        <input v-model="start_date" type="date">
                    </div>
                <hr>
                </div>
                <div class="form-group col-md-4">
                    <div>
                        <label>Select final date</label>
                        <input v-model="finish_date" type="date">
                        <hr>
                    </div>
                </div>
                <div class="col-md-4">
                <hr>
                <div class="form-group">
                    <label for="value">Value:</label>
                    <br>
                    <input v-model.number="selectedValueQ" id="value"
                           type="number" min="0" max="999999999"
                           placeholder="Your limit" pattern="^\d+(\.\d+)?$" required>
                </div>
                <hr>
                <div>
                    <button v-on:click="setLimitArb"
                        :variant="secondary"
                        class="btn btn-outline-primary"
                        :disabled="isValidDataArb===false">Set limit
                    </button>
                    <br>
                    <button v-on:click="createDone" :variant="secondary" v-show="isDone" class="btn btn-outline-primary">
                        {{msg}}
                    </button>
                </div>
            </div>
            </div>



        </div>
    </div>
</template>


<script>
    import axios from 'axios';

    var today = new Date();
    var UTC = -today.getTimezoneOffset() / 60;
    var yyyy = today.getFullYear();

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
                isDone: false,
                msg: '',
                spending_list: [],
                fixed: null,
                yyyy: yyyy,
                selectedYear: null,
                selectedMonth: null,
                selectedValue: null,
                start_date: null,
                finish_date: null,
                selectedSpending: null,
                errors: [],
                UTC: null,
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
                }).then(response => (this.msg = response.data)
                );
                 this.$router.go('/spendings/limit_ind')
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
                }).then(response => (this.msg = response.data));
                this.isDone = true;
            },
            setLimitArb: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/set_limit_arb/',
                    data: {
                        'spending_id': this.selectedSpending,
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'UTC': UTC,
                        'value': this.selectedValueQ
                    }
                }).then(response => (this.msg = response.data));
                this.isDone = true;
            },
            createDone: function (event) {
                this.$router.go('/spendings/limit_ind')
            },
        }
    }
</script>

<style scoped>

</style>
