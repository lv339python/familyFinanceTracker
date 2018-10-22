<template>
    <div id="spending_history">
        <div>
            <div class="form-group col-md-5" >
                <div>
                    <label>Select the start date</label>
                    <input v-model="start_date" type="date">
                </div>
                <hr>
            </div>
            <div class="form-group col-md-5">
                <div>
                    <label>Select the final date</label>
                    <input v-model="finish_date" type="date">
                    <hr>
                </div>
            </div>
            <div class="col-md-5" v-if="start_date<finish_date">
                <button v-on:click="createHistory" :variant="secondary">Show all spending</button>
            </div>
        </div>
        <div v-show="isCategory&&(start_date<=finish_date)" class="col-md-6">
            <select v-model="selected" class="form-control">
                <option disabled value="">Spending during period...</option>
                <option v-for="spend in spending_history_individual"
                    v-bind:value="spend.history" > {{ spend.spending}}
                </option>
                <option v-for="spend in spending_history_admin"
                    v-bind:value="spend.history"> {{ spend.spending}}
                </option>
            </select>
            <br>
            <div v-show="selected&&(start_date<=finish_date)" >
                <table class="table table-bordered" >
                    <thead>
                        <tr>
                            <th v-for="(value, key) in selected[0]">{{key}}</th>
                        </tr>
                    </thead>
                    <tbody  v-for="(values, keys) in selected">
                        <tr>
                            <td  v-for="value_one in values">{{ value_one }}</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>

</template>

<script>
var x = new Date()
var UTC= -x.getTimezoneOffset()/60

import axios from 'axios';

export default {
    name: "Spending_history",
    data () {
        return {
            isCategory: false,
            start_date: null,
            finish_date: null,
            selected: '',
            spending_history_individual: {
            },
            spending_history_admin: {
            },
            msg:'',
            UTC: null

        }
    },
    methods: {
        createHistory: function (event) {
            axios({
                method: 'post',
                url: '/api/v1/spending_history/show/',
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
    }
}
</script>

<style scoped>
</style>
