<template>
    <div class="Income_tracker">
        <div class="wrapper">
            <div id="total">
                <p>The total amount of income from the 1-st of this month till today is {{this.cur_income}}</p>
            </div>
            <div id="form">
                <p>Please choose dates below:</p>
                <p>Start date:</p>
                <input v-model="start_date" type="date" required>
                <p>End date:</p>
                <input v-model="end_date" type="date" required>
                <p>
                    <button v-on:click="sub_dates">submit</button>
                </p>
            </div>

            <div id="result">
                <table border='1px' v-if="shownResult">
                    <caption>All the incomes for the chosen period:</caption>
                    <tr>
                        <th>Income</th>
                        <th>Fund</th>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Comments</th>
                    </tr>
                    <tr v-for="item in paginatedData">
                        <td>{{item['income']}}</td>
                        <td>{{item['fund']}}</td>
                        <td>{{item['date']}}</td>
                        <td>{{item['amount']}}</td>
                        <td>{{item['comment']}}</td>
                    </tr>
                </table>
                <div v-show="pageCount>1">
                    <button :disabled="paginated_page_number === 0" @click="prevPage"> Previous
                    </button>
                    <button :disabled="paginated_page_number>= pageCount -1 " @click="nextPage"> Next
                    </button>
                </div>
                <p>
                    <button v-on:click="reRender" v-if="shownResult">refresh</button>
                </p>
            </div>

        </div>
        <div class="chartcontainer" v-if="shownResult">
                    <Income_chart
                        v-bind:date_to_props="make_list_dates"
                        v-bind:amount_to_props="make_list_amounts">
                    </Income_chart>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Income_chart from 'src/components/examples/Income_chart';


    export default {
        name: "Income_tracker",
        components: {"Income_chart": Income_chart},
        data() {
            return {
                start_date: '',
                end_date: '',
                list_with_incomes: '',
                shownResult: false,
                cur_income: 0,
                // this is the size of a paginated page
                pagination_size: 3,
                paginated_page_number: 0,
                //this is the time which is added to the user provided date
                start_date_time: "T00:00:00",
                end_date_time: "T23:59:59",
                date_to_props: [],
                amount_to_props: [],
                income_to_props: []
                //fund_to_props: []
            }
        },
        created() {
            axios.get('api/v1/income_history/get_cur_incomes/')
                .then(response => {
                    this.cur_income = response.data;
                })
                .catch(e => {
                    alert(error.response.data);
                });
        },

        computed: {
            pageCount() {
                let l = this.list_with_incomes.length,
                    s = this.pagination_size,
                    pageMax = (l % s != 0) ? Math.floor(l / s) + 1 : Math.floor(l / s);
                return pageMax;
            },
            paginatedData() {
                const start = this.paginated_page_number * this.pagination_size,
                    end = (start + this.pagination_size <= this.list_with_incomes.length) ? start + this.pagination_size : this.list_with_incomes.length;
                return this.list_with_incomes
                    .slice(start, end);
            },
            make_list_dates(){
                let funds = this.list_with_incomes[this.list_with_incomes.length-1];
                let dates_for_funds = [];
                for (var item in funds){
                    let temp = {};
                    let list_in_list = [];
                    for (var val in this.list_with_incomes){
                        if (funds[item]==this.list_with_incomes[val]['fund']){
                            list_in_list.push(this.list_with_incomes[val]['date']);
                        }
                    }
                    temp[funds[item]] = list_in_list;
                    dates_for_funds.push(temp);
                }
                this.date_to_props = dates_for_funds;
                return this.date_to_props

            },
            make_list_amounts(){
                let funds = this.list_with_incomes[this.list_with_incomes.length-1];
                let amounts_for_funds = [];
                for (var item in funds){
                    let temp = {};
                    let list_in_list = [];
                    for (var val in this.list_with_incomes){
                        if (funds[item]==this.list_with_incomes[val]['fund']){
                            list_in_list.push(this.list_with_incomes[val]['amount']);
                        }
                    }
                    temp[funds[item]] = list_in_list;
                    amounts_for_funds.push(temp);
                }
                this.amount_to_props = amounts_for_funds;
                return this.amount_to_props
            },
            make_list_incomes(){
                let funds = this.list_with_incomes[this.list_with_incomes.length-1];
                let incomes_for_funds = [];
                for (var item in funds){
                    let temp = {};
                    let list_in_list = [];
                    for (var val in this.list_with_incomes){
                        if (funds[item]==this.list_with_incomes[val]['fund']){
                            list_in_list.push(this.list_with_incomes[val]['income']);
                        }
                    }
                    temp[funds[item]] = list_in_list;
                    incomes_for_funds.push(temp);
                }
                this.income_to_props = incomes_for_funds;
                return this.income_to_props
            },
            // make_list_funds(){
            //     var item;
            //     for (item in this.list_with_incomes){
            //         this.fund_to_props.push(this.list_with_incomes[item]['fund']);
            //     }
            //     return this.fund_to_props
            // },

        },


        methods: {
            sub_dates: function () {
                if (this.start_date.length != 0 && this.end_date.length != 0) {
                    this.shownResult = true;
                    axios({
                        method: "post",
                        url: "api/v1/income_history/track/",
                        data: {
                            'start': this.start_date + this.start_date_time,
                            'end': this.end_date + this.end_date_time
                        }
                    }).then(response => {
                        this.list_with_incomes = response.data;
                    }).catch(error => {
                        console.log(error.response.data);
                    })
                } else {
                    alert('You did not choose any dates or you chose only one date out of two required! Choose both dates!')
                }
                ;
            },
            reRender: function () {
                {
                    this.$router.go('api/v1/income_history/track/');
                }
            },
            nextPage() {
                this.paginated_page_number++;
            },
            prevPage() {
                this.paginated_page_number--;
            }
        }
    }
</script>

<style>
    .wrapper {
        display: flex;
        flex-direction: column;
        margin: 0px auto;

    }

    caption {
        caption-side: top;
    }

    .Income_tracker {
        display: flex;
    }

    div #chartcontainer{
        margin-right: 600px;
    }
</style>
