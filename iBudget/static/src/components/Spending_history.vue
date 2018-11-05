<template>
    <div id="spending_history">
        <div>
            <div id='total' class="col-md-6">
                <h6>Total in this month:
                    <br>
                    {{total}}
                </h6>
                <hr>
            </div>
            <div class="form-group col-md-6">
                <div>
                    <label>Select start date</label>
                    <input v-model="start_date" type="date" @change="blockButtom()">
                </div>
                <hr>
            </div>
            <div class="form-group col-md-6">
                <div>
                    <label>Select final date</label>
                    <input v-model="finish_date" type="date" @change="blockButtom()">
                    <hr>
                </div>
            </div>
            <div class="col-md-5" v-if="start_date<=finish_date">
                <button class="btn btn-outline-warning" v-on:click="createHistory" :variant="secondary">Show all
                    spending
                </button>
            </div>
        </div>
        <div v-show="isCategory&&(start_date<=finish_date)" class="col-md-6">
            <div class="btn-group" role="group" v-model="selected">
                <button v-for="spend in spending_history_individual"
                        type="button"
                        class="btn btn-outline-success"
                        v-bind:value="spend.history"
                        v-on:click="dataPaginated(spend.history)">
                    {{ spend.spending}}
                </button>
                <button v-for="spend in spending_history_admin"
                        type="button"
                        class="btn btn-outline-success"
                        v-bind:value="spend.history"
                        v-on:click="dataPaginated(spend.history)">
                    {{ spend.spending}}
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
                        <td v-if="p.member">{{ p.member}}</td>
                        <td>{{ p.value}}</td>
                        <td>{{ p.date }}</td>
                        <td>{{ p.fund }}</td>
                    </tr>
                    </tbody>
                </table>
                <div v-show="pageCount>1">
                    <button class="btn btn-outline-secondary" :disabled="pageNumber === 0" @click="prevPage"> Previous
                    </button>
                    <button class="btn btn-outline-secondary" :disabled="pageNumber >= pageCount -1 " @click="nextPage">
                        Next
                    </button>
                </div>
            </div>
        </div>
        <button class="btn btn-outline-warning" v-on:click="createFile" :variant="secondary">Download history
        <!--<a v-bind:href="'/api/v1/spending_history/create/?start_date=' + start_date + '&ed=' + finish_date + '&utc=' + UTC">Download </a>-->
            <a :href="'/api/v1/spending_history/download_file/?start_date=' + start_date + '&finish_date=' + finish_date + '&utc=' + UTC">Download </a>
        </button>
    </div>
</template>

<script>
    var x = new Date()
    var UTC = -x.getTimezoneOffset() / 60

    import axios from 'axios';
    import saveAs from 'file-saver';

    export default {
        name: "Spending_history",
        data() {
            return {
                total: 0,
                isCategory: false,
                listValues: [],
                pageNumber: 0,
                size: 2,
                start_date: new Date().toJSON().slice(0,10),
                finish_date: new Date().toJSON().slice(0,10),
                selected: [],
                spending_history_individual: {},
                spending_history_admin: {},
                errors: [],
                UTC: null
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
            dataPaginated: function (spending_data) {
                this.selected = spending_data;
                this.pageNumber = 0;
                this.listValues = spending_data;
            },
            showTotal: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending_history/create/',
                    data: {
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'UTC': UTC
                    }
                })
                    .then(response => {
                        this.spending_history_admin = response.data.admin;
                        this.spending_history_individual = response.data.individual;
                        this.isCategory = true

                    })
                    .catch(e => {
                        this.errors.push(e)
                    })
            },
            createFile: function (event) {
                axios({
                    method: 'get',
                    url: '/api/v1/spending_history/download_file/',
                    data: {
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'UTC': UTC
                    },
                })
                    .then((function(response) {
                        // let blob = new Blob([response.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' }),
                        //     url = window.URL.createObjectURL(blob);
                        // window.open(url)

                        // function s2ab(s) {
                        //   var buf = new ArrayBuffer(s.length);
                        //   var view = new Uint8Array(buf);
                        //   for (var i=0; i!=s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
                        //   return buf;
                        // }

                        let blob = new Blob([response.data], { type:'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'});
                        let FileSaver = require('file-saver');
                        FileSaver.saveAs(blob, "hello world.xlsx");

                        // let file = new File([response.data], "hello world.xlsx", {type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"});
                        // FileSaver.saveAs(file);

                        // let link = document.createElement('a');
                        // link.href = window.URL.createObjectURL(blob);
                        // link.download = 'Report.xlsx';
                        // link.click()
                    }))
                    .catch(e => {
                        this.errors.push(e)
                    })
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
                        'UTC': UTC
                    }
                })
                    .then(response => {
                        this.spending_history_admin = response.data.admin;
                        this.spending_history_individual = response.data.individual;
                        this.isCategory = true

                    })
                    .catch(e => {
                        this.errors.push(e)
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
    #total {
        text-align: center
    }
    #spending_history {

    }
</style>
