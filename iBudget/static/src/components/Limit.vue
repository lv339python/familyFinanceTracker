<template>
    <div id="limit">
        <div class="wrapper">
            <div id="available_spendings" v-if="brand_new_user">
                <p>You want to set limits by day or by month/year? Choose below:</p>
                <form v-on:change="set_date_choice">
                    <input type="radio" value="True" v-model="picked"> monthly/yearly limits
                    <input type="radio" value="False" v-model="picked"> daily limits
                </form>
            </div>

            <div id="limit_values" v-if="!brand_new_user">
                <div id="daily" v-if="daily">
                    <p>You can set limits for the following group spendings:
                        <select v-model="spending_category" required>
                            <option v-for="item in list_of_spendings">{{item}}</option>
                        </select>
                    </p>
                    <form>
                        <p>Start date:</p>
                        <input v-model="start_date" type="date" placeholder="yyyy-mm-dd"
                               required size="9">
                        <p>End date:</p>
                        <input v-model="end_date" type="date" placeholder="yyyy-mm-dd"
                               required size="9">
                        <p>Amount:</p>
                        <input v-model="value" type="number" required>
                    </form>
                    <p>
                        <button v-on:click='set_limit_daily'>set limit</button>
                    </p>
                </div>

                <div id="monthly_yearly" v-if="!daily">
                    <p>You can set limits for the following group spendings:
                        <select v-model="spending_category" required>
                            <option v-for="item in list_of_spendings">{{item}}</option>
                        </select>
                    </p>
                    <form>
                        <p>Year:</p>
                        <select v-model="year" required>
                            <option v-for="item in 10">{{yyyy-1 + item}}</option>
                        </select>
                        <p>Month:</p>
                        <select v-model="month" required>
                            <option v-for="month in months" v-bind:value="month.valueM"> {{ month.nameM }}</option>
                        </select>
                        <p>Value:</p>
                        <input v-model="value" type="number" required>
                    </form>
                    <p>
                        <button v-on:click='set_limit_year'>set limit</button>
                    </p>
                </div>
            </div>
            <p>{{reply}}</p>
            <p>
                <button v-show='isShown' v-on:click="reRender">OK</button>
            </p>
        </div>
    </div>

</template>

<script>
    import axios from 'axios';
    var today = new Date();
    var yyyy = today.getFullYear();


    export default {
        name: "Limit",
        data() {
            return {
                list_of_spendings: [],
                start_date: '',
                end_date: '',
                value: '',
                spending_category: '',
                reply: '',
                isShown: false,
                brand_new_user: null,
                picked: '',
                daily:null,
                year: null,
                month:null,
                yyyy: yyyy,
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
                ]
            }
        },
        created() {
            axios.get('api/v1/spending/admin/limit/')
                .then(response => {
                    this.list_of_spendings = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('api/v1/spending/admin/check_choice/')
                .then(response => {
                    if(response.data === 'True'){
                        this.brand_new_user = false;
                        this.daily = false
                    }
                    else {
                        this.brand_new_user = true;
                        this.daily = false

                    }
                })
                .catch(e => {
                    console.log(e.response.data)
                })
        },
        methods: {
            set_limit_daily: function (event) {
                axios({
                    method: 'post',
                    url: 'api/v1/spending/admin/set_limit/',
                    data: {
                        'spending_category': this.spending_category,
                        'start_date': this.start_date,
                        'end_date': this.end_date,
                        'value': this.value,
                    },
                }).then(response => {
                    this.reply = response.data;
                    this.isShown = true
                })
                    .catch(function (error) {
                        alert(error.response.data);
                    });
            },
            set_limit_year: function (event) {
                var days_in_month = new Date(this.year, this.month, 0).getDate();
                if(this.month ===0){
                    axios({
                    method: 'post',
                    url: 'api/v1/spending/admin/set_limit/',
                    data: {
                        'spending_category': this.spending_category,
                        'start_date': this.year + '-' + '01' + '-' + '01',
                        'end_date': this.year + '-' + '12' + '-' + '31',
                        'value': this.value,
                    },
                    }).then(response => {
                        this.reply = response.data;
                        this.isShown = true
                    })
                        .catch(function (error) {
                            alert(error.response.data);
                        });
                    return
                }
                axios({
                    method: 'post',
                    url: 'api/v1/spending/admin/set_limit/',
                    data: {
                        'spending_category': this.spending_category,
                        'start_date': this.year + '-' + this.month + '-' + '01',
                        'end_date': this.year + '-' + this.month + '-' + days_in_month,
                        'value': this.value,
                    },
                }).then(response => {
                    this.reply = response.data;
                    this.isShown = true
                })
                    .catch(function (error) {
                        alert(error.response.data);
                    });
            },
            reRender: function (event) {
                if (this.isShown = true) {
                    this.$router.go('api/v1/spending/admin/set_limit/');
                }
            },
            set_date_choice: function (event) {
                this.brand_new_user = false;
                alert(this.picked);
                axios({
                    method: 'post',
                    url: 'api/v1/spending/admin/set_choice/',
                    data: {
                        'choice': this.picked,
                    },
                }).then(response => {
                    alert(response.data)
                })
                    .catch(function (error) {
                        alert(error.response.data);
                    });
            }

        }
    }
</script>

<style scoped>
    .wrapper {
        display: flex;
        flex-direction: column;
        margin: 0px auto;
    }

    .limit {
        display: flex;
    }

</style>
