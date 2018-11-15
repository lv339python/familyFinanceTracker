<template>
    <div class="Income_tracker">
        <div class="wrapper">
            <div id="total">
                <h3>The total amount of income from the 1-st of this month till today is {{this.cur_income}}</h3>
            </div>

            <b-form v-if="!shownResult" class="income-tracker-form">
                <b-form-group label="Start date:"
                              label-for="start-date"
                              description="Please choose the start date">
                    <b-form-input v-model="start_date" id="start-date" type="date" required></b-form-input>
                </b-form-group>
                <b-form-group label="End date:"
                              label-for="end-date"
                              description="Please choose the end date">
                    <b-form-input v-model="end_date" id="end-date" type="date" required></b-form-input>
                </b-form-group>
                <b-button v-on:click="sub_dates" type="submit" variant="primary">
                    Submit
                </b-button>

            </b-form>


            <div id="result">
                <table border='1px' v-if="shownResult">
                    <caption>All the incomes for the chosen period:</caption>
                    <tr>
                        <th>Income</th>
                        <th>Fund</th>
                        <th>Date</th>
                        <th>Amount</th>
                        <th>Comments</th>
                        <th>Delete</th>
                    </tr>
                    <tr v-for="item in paginatedData">
                        <td>{{item['income']}}</td>
                        <td>{{item['fund']}}</td>
                        <td>{{item['date']}}</td>
                        <td>{{item['amount']}}</td>
                        <td>{{item['comment']}}</td>
                        <td>
                            <button
                                type="button" class="btn btn-outline-danger"
                                v-on:click="deleteIncomeHistory(item['income_history_id'])"
                                :variant="secondary">Delete
                            </button>
                        </td>
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
                <div class="download_buttons" v-if="!no_result">
                <a v-bind:href='"/api/v1/income_history/download_xlsx_file/?start_date=" + start_date + start_date_time  + "&finish_date=" +  end_date +
                end_date_time + "&UTC=" + UTC'>
                    <button :variant="seconadary" :disabled="shownResult===false||(end_date<start_date)">
                        Download xlsx
                    </button>
                </a>
                <a v-bind:href='"/api/v1/income_history/download_csv_file/?start_date=" + start_date + start_date_time + "&finish_date=" +
                  end_date + end_date_time + "&UTC=" + UTC'>
                    <button :variant="seconadary" :disabled="shownResult===false||(end_date<start_date)">
                        Download csv
                    </button>
                </a>
            </div>
            </div>

            <div id="no_result" v-if="no_result">
                <p>There are no incomes within the chosen time frame!</p>
                <p>
                    <button v-on:click="reRender">refresh</button>
                </p>
            </div>
        </div>
        <div class="chartcontainer" v-if="shownResultChart">
            <!--v-if is necessary to render the chart correctly, because computed is called with default
            data first and the chart is not rendered; here it's called twice and only the valid result is
            rendered-->
            <Income_chart v-if="make_list_dates.length !== 0"
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
                start_date: new Date().toJSON().slice(0, 10),
                end_date: new Date().toJSON().slice(0, 10),
                list_with_incomes: '',
                shownResult: false,
                UTC: -new Date().getTimezoneOffset() / 60,
                shownResultChart: false,
                cur_income: null,
                // this is the size of a paginated page
                pagination_size: 3,
                paginated_page_number: 0,
                //this is the time which is added to the user provided date
                start_date_time: "T00:00:00",
                end_date_time: "T23:59:59",
                date_to_props: [],
                amount_to_props: [],
                no_result: false,
                last_element: null
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
                    pageMax = (l % s !== 0) ? Math.floor(l / s) + 1 : Math.floor(l / s);
                return pageMax;
            },
            paginatedData() {
                const start = this.paginated_page_number * this.pagination_size,
                    end = (start + this.pagination_size <= this.list_with_incomes.length) ? start + this.pagination_size : this.list_with_incomes.length - 2;
                // this.list_with_incomes.splice(this.list_with_incomes.length-1, 1);
                //                 console.log("##", this.list_with_incomes);

                return this.list_with_incomes.slice(start, end);
            },
            make_list_dates() {
                this.recover_list();
                let funds = this.list_with_incomes[this.list_with_incomes.length - 1];
                let dates_for_funds = [];
                for (var item in funds) {
                    let temp = {};
                    let list_in_list = [];
                    for (var val in this.list_with_incomes) {
                        if (funds[item] === this.list_with_incomes[val]['fund']) {
                            list_in_list.push(this.list_with_incomes[val]['date']);
                        }
                    }
                    temp[funds[item]] = list_in_list;
                    dates_for_funds.push(temp);
                }
                this.date_to_props = dates_for_funds;
                return this.date_to_props

            },
            make_list_amounts() {
                let funds = this.list_with_incomes[this.list_with_incomes.length - 1];
                let amounts_for_funds = [];
                for (var item in funds) {
                    let temp = {};
                    let list_in_list = [];
                    for (var val in this.list_with_incomes) {
                        if (funds[item] === this.list_with_incomes[val]['fund']) {
                            list_in_list.push(this.list_with_incomes[val]['amount']);
                        }
                    }
                    temp[funds[item]] = list_in_list;
                    amounts_for_funds.push(temp);
                }
                this.amount_to_props = amounts_for_funds;
                return this.amount_to_props
            },
        },


        methods: {
            sub_dates: function () {
                if (this.start_date.length !== 0 && this.end_date.length !== 0) {
                    axios({
                        method: "post",
                        url: "api/v1/income_history/track/",
                        data: {
                            'start': this.start_date + this.start_date_time,
                            'end': this.end_date + this.end_date_time,
                            'time_diff': this.UTC
                        }
                    }).then(response => {
                        this.list_with_incomes = response.data;
                        this.last_element = this.list_with_incomes[this.list_with_incomes.length - 1];
                        //if we got empty JSON with empty list inside
                        if (this.list_with_incomes.length === 1) {
                            this.no_result = true;
                        }
                        //if we got JSON with only one array inside, not enough to draw a chart
                        else if (this.list_with_incomes.length === 2) {
                            this.shownResult = true;
                        }
                        else {
                            this.shownResult = true;
                            this.shownResultChart = true
                        }

                    }).catch(error => {
                        console.log(error.response.data);
                    })
                } else {
                    alert('You did not choose any dates or you chose only one date out of two required! Choose both dates!')
                }
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
            },
            recover_list() {
                this.list_with_incomes = this.list_with_incomes.concat([this.last_element]);
            },
            deleteIncomeHistory: function (IncHistory) {
                axios({
                    method: 'delete',
                    url: '/api/v1/income_history/delete_income_history/' + IncHistory,
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.$router.go('api/v1/income_history/track/')
                }).catch(error => {
                    alert(error.response.data)
                })

            }
        }
    }

</script>

<style>
    input, label {
        display: block;
    }

    .wrapper {
        display: flex;
        flex-direction: column;
        margin: 0 auto;
        justify-content: left;
    }

    caption {
        caption-side: top;
    }

    .Income_tracker {
        display: flex;
        height: 100%;
    }

    div #chartcontainer {
        margin-right: 600px;
        width: 800px;
    }

    #no_result {
        margin-top: 50px;

    }

    .income-tracker-form {
        width: 20%;
        margin: 0 auto;
    }
    .download_buttons{
        margin: auto;
        margin-top: 5px;
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        width: max-content;
    }
</style>
