<template>
    <div id="spend">
        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Chose your goal:</label>
                <select v-model="fund" class="form-control">
                    <option v-for="fund in fund_list_ind" v-bind:value="fund.id"> {{ fund.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Chose group</label>
                <select v-model="group" class="form-control">
                    <option v-for="group in group_list"
                            v-bind:value="group.id"
                            v-on:click="is_active_shared_fund=group.id">
                        {{ group.name }}
                    </option>
                </select>
            </div>
            <hr>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Chose your group goal</label>
                <select v-model="fund" class="form-control">
                    <option v-for="fund in fund_list"
                            v-if="fund.id_group === is_active_shared_fund"
                            v-bind:value="fund.id_fund">
                        {{fund.name_fund}}
                    </option>
                </select>
            </div>
            <hr>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Start date</label>
                <input v-model="start_date" type="date">
            </div>
            <hr>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Finish date</label>
                <input v-model="finish_date" type="date">
            </div>
            <hr>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Input value</label>
                <input v-model="value" type="number" min="1" class="form-control">
            </div>
        </div>
        <div v-show="isValidData">
            <button v-on:click="setData" :variant="secondary">Save</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Financial_goal",
        data() {
            return {
                fund_list: [],
                fund_list_ind: [],
                group_list: null,
                fund: null,
                start_date: null,
                finish_date: null,
                value: null,
                is_active_shared_fund: null
            }
        },

        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.fund_list != null &&
                        this.fund_list_ind != null &&
                        this.start_date != null &&
                        this.finish_date != null &&
                        this.value != null &&
                        this.start_date < this.finish_date;
                    return result;
                }
            }
        },

        created() {
            axios.get('/api/v1/fund/users_shared_fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list_ind = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/group/get_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.group_list = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                });
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/fund/register_financial_goal/',
                    data: {
                        'value': this.value,
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'fund': this.fund
                    }
                }).then(response => {
                    this.$router.go('fund/register_financial_goal')
                })
            }
        }
    }
</script>

<style scoped>

</style>
