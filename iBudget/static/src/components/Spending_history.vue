<template>
    <div id="spending_history">
        <div>
            <div class="col-md-8 total">
                <h6>Total in this month:
                    <br>
                    {{total}}
                </h6>
                <hr>
            </div>
            <div class="form-group col-md-8">
                <div class="dates">
                    <label>Select start date</label>
                    <input v-model="start_date" type="date" @change="blockButtom()">
                    <label>Select final date</label>
                    <input v-model="finish_date" type="date" @change="blockButtom()">
                    <hr>
                </div>
            </div>
            <div class="col-md-8 total">
                <button class="btn btn-outline-warning"
                    :disabled="start_date>finish_date"
                    v-on:click="createHistory"
                    :variant="secondary">
                        Show all spending
                </button>
            </div>
        </div>
        <div v-show="isCategory&&(start_date<=finish_date)" class="col-md-8 total">
            <div class="btn-group-justified  but-fl" role="group" v-model="selected" v-if="spending_all.length!==0">
                <button v-for="spend in spending_all"
                        type="button"
                        class="btn btn-outline-success but-w"
                        v-bind:value="spend.history"
                        v-on:click="dataPaginated(spend.history)"
                        data-toggle="tooltip"
                        v-bind:title="spend.spending">
                    {{ buttonName(spend.spending)}}
                </button>
            </div>
            <hr>
            <div v-show="selected&&(start_date<=finish_date)">
                <table class="table table-bordered">
                    <thead>
                    <tr>
                        <th v-for="(value, key) in selected[0]">{{ key }}</th>
                    </tr>
                    </thead>
                    <tbody v-for="p in paginatedData">
                    <tr>
                        <td v-if="p.member">{{p.member}}</td>
                        <td>{{ p.value }}</td>
                        <td>{{ p.date }}</td>
                        <td>{{ p.fund }}</td>
                        <td >
                            <button
                                    type="button" class="btn btn-outline-danger" v-on:click="deleteHistory(p.Delete)"
                                    :variant="secondary">Delete
                            </button>
                        </td>
                    </tr>
                    </tbody>
                </table>
                <div v-show="pageCount>1" class='prevNext'>
                    <b style="word-space:2em">&nbsp;</b>
                    <button :disabled="pageNumber===0" @click="prevPage"> Previous</button>
                    <span v-if="pageNumber > 0 && pageNumber < pageCount-1">
                        1... <b>{{pageNumber +1 }}</b> ... {{pageCount}}
                    </span>
                    <span v-if="pageNumber===0">
                        <b> 1 </b> ... <b style="word-space:2em">&nbsp;</b> ... {{pageCount}}
                    </span>
                    <span v-if="pageNumber===pageCount-1">
                        1  ... <b style="word-space:2em">&nbsp;</b> ... <b>{{pageCount}}</b>
                    </span>
                    <button :disabled="pageNumber >= pageCount-1 " @click="nextPage"> Next</button>
                    <b style="word-space:2em">&nbsp;</b>
                </div>
            </div>
            <div  v-if="hasData==0">

                <h5>There are no spending during this period...</h5>
            </div>
        </div>
        <div class="download_buttons form-group col-md-6">
            <hr>
            <a v-bind:href='"/api/v1/spending_history/download_xlsx_file/?start_date=" + start_date + "&finish_date=" +  finish_date + "&UTC=" + UTC'>
                <button class="btn btn-outline-warning" :disabled="isCategory===false||(finish_date<start_date)"
                        :variant="secondary">Download xlsx
                </button>
            </a>
            <a v-bind:href='"/api/v1/spending_history/download_csv_file/?start_date=" + start_date + "&finish_date=" +  finish_date + "&UTC=" + UTC'>
                <button class="btn btn-outline-warning" :disabled="isCategory===false||(finish_date<start_date)"
                        :variant="secondary">Download csv
                </button>
            </a>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    var UTC = -new Date().getTimezoneOffset() / 60;
    export default {
        name: "Spending_history",
        data() {
            return {
                total: 0,
                isCategory: false,
                listValues: [],
                pageNumber: 0,
                size: 2,
                start_date: new Date().toJSON().slice(0, 10),
                finish_date: new Date().toJSON().slice(0, 10),
                selected: [],
                spending_history_individual: {},
                spending_history_admin: {},
                spending_all: [],
                errors: [],
                hasData: null,
                UTC: -new Date().getTimezoneOffset() / 60
            }
        },
        created() {
            axios({
                method: 'get',
                url: '/api/v1/spending_history/show/'
            })
                .then(response => {
                    this.total = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            buttonName: function (name) {
                if (name.length > 9) {
                    name = name.slice(0, 9) + "..."
                }
                return name
            },
            dataPaginated: function (spending_data) {
                this.selected = spending_data;
                this.pageNumber = 0;
                this.listValues = spending_data;
            },
            blockButtom: function () {
                this.isCategory = false;
                this.listValues = [];
                this.selected = [];
                this.spending_history_individual = {};
                this.spending_history_admin = {};
            },
            createHistory: function (event) {
                this.isCategory = false;
                this.listValues = [];
                this.selected = [];
                this.spending_history_individual = {};
                this.spending_history_admin = {};
                axios({
                    method: 'post',
                    url: '/api/v1/spending_history/create/',
                    data: {
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'UTC': UTC,
                    }
                })
                .then(response => {
                    this.spending_history_admin = response.data.admin;
                    this.spending_history_individual = response.data.individual;
                    this.spending_all = this.spending_history_individual.concat(this.spending_history_admin);
                    this.isCategory = true;
                    this.hasData = this.spending_all.length

                })
                .catch(e => {
                    this.errors.push(e)
                })
            },
             deleteHistory: function (spendHistory) {
                axios({
                    method: 'delete',
                    url: '/api/v1/spending_history/delete_spending_history/' + spendHistory,

                }).then(response => {
                        this.reply = response.data;
                        alert(this.reply);
                        this.$router.go('/spendings/history')
                    }).catch(error => {
                        alert(error.response.data)
                    })

            },
            nextPage() {
                this.pageNumber++;
            },
            prevPage() {
                this.pageNumber--;
            }
        },
        computed: {
            pageCount() {
                let l = this.listValues.length,
                    s = this.size,
                    pageMax = (l % s != 0) ? Math.floor(l / s) + 1 : Math.floor(l / s);
                return pageMax;
            },
            paginatedData() {
                const start = this.pageNumber * this.size,
                    end = (start + this.size <= this.listValues.length) ? start + this.size : this.listValues.length;
                return this.listValues
                    .slice(start, end);
            }
        }
    }
</script>

<style scoped>
    .total {
        text-align: center
    }

    .dates {
        text-align: center;
        justify-content: space-around;
    }
    #spending_history {

    }

    .but-fl {
        display: flex;
        flex-wrap: wrap;
        margin: 10px;
        justify-content: flex-start;
    }

    .but-w {
        white-space: normal !important;
        word-wrap: break-word;
        width: 16.5%
    }
</style>
