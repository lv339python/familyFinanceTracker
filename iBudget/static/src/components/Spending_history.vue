<template>
    <div id="spending_history">
        <div>
            <div class="form-group col-md-4" >
                <div>
                    <label>Select the start date</label>
                    <hr>
                    <input v-model="start_date" type="date">
                </div>
            </div>
            <div class="form-group col-md-4">
                <div>
                    <label>Select the final date</label>
                    <hr>
                    <input v-model="finish_date" type="date">
                </div>
            </div>
            <div>
                <button v-on:click="createHistory" :variant="secondary">Show all spending</button>
            </div>
        </div>
        <div v-show="isCategory">
            <select v-model="selected" class="form-control col-md-4">
                <option v-for="spend in spending_history_individual"
                    v-bind:value="spend.history" > {{ spend.spending}}
                </option>
                <option v-for="spend in spending_history_admin"
                    v-bind:value="spend.history"> {{ spend.spending}}
                </option>
            </select>
            <div v-show="selected" >
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
            isDone: false,
            isCategory: false,
            isAdmin: false,
            isMember: false,
            start_date: null,
            finish_date: null,
            selected: '',
            spending_list: [],
            spending_history: {
            },
            spending_history_individual: {
            },
            spending_history_admin: {
            },
            msg:'',
            UTC:null

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
                this.spending_history = response.data;
                this.spending_history_admin = response.data.admin;
                this.spending_history_individual = response.data.individual;
                this.isCategory = true

            })
            .catch(e => {
                this.errors.push(e)
            })
        },
        member: function (event) {
            this.isMember =true;
            this.isAdmin=false;
            console.log('member')
        },

        admin: function(event){
            this.isAdmin =true;
            this.isMember=false
        },
    }
}
</script>

<style scoped>
</style>
