<template>
    <div class="cont">
        <div class="form-group">
            <label>Select income category:</label>
            <select v-model="inc_category" class="form-control">
                <option v-for="income in income_list" v-bind:value="income.id"> {{ income.name }}
                </option>
            </select>
        </div>
        <div class="form-group" v-if="is_shared===false">
            <label>Choose your fund:</label>
            <select v-model="fund_category" class="form-control">
                <option v-for="fund in fund_list" v-bind:value="fund.id"> {{ fund.name }}
                </option>
            </select>
        </div>
        <div class="form-group" v-else>
            <label>Chose group</label>
            <select v-model="group" class="form-control">
                <option v-for="group in group_list"
                        v-bind:value="group.id"
                        v-on:click="is_active_group=group.id">
                    {{ group.name }}
                </option>
            </select>
        </div>
        <div class="form-group" v-if="is_active_group !== null && is_shared===true">
            <label>Chose category</label>
            <select v-model="fund_category" class="form-control">
                <option v-for="fund in shared_list"
                        v-if="fund.id_group === is_active_group"
                        v-bind:value="fund.id_fund">
                    {{fund.name_fund}}
                </option>
            </select>
        </div>
        <div class="form-group">
            <b-form-checkbox id="shared_button" v-model=
                "is_shared">Choose among shared funds :
            </b-form-checkbox>
        </div>
        <div class="form-group">
            <label>Input sum of your income </label>
            <input v-model="value" type="number" min="1" class="form-control">
        </div>
        <div >
            <div class="form-group">
                <label>Input comment</label>
                <input v-model="comment" type="text" class="form-control">
            </div>
        </div>

        <div class="form-group">
            <label>Choose date</label>
            <input v-model="date" type="date">
        </div>

        <div>
            <b-button :disabled="DataValidation===false" class="btn btn-outline-primary"
                      @click="setData" :variant="success">Save
            </b-button>
        </div>

        <div>
            <b-button class="btn btn-outline-danger" @click="clear" :variant="warning">Clear form</b-button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "income_history",
        data() {
            return {
                income_list: [],
                fund_list: [],
                group_list: [],
                shared_list: [],
                inc_category: null,
                fund_category: null,
                value: null,
                date: null,
                comment: '',
                is_active_group: null,
                is_shared: false
            }
        },
        computed: {
            DataValidation: {
                get: function () {
                    let result =
                        this.inc_category != null &&
                        this.fund_category != null &&
                        this.value != null &&
                        this.date != null;
                    return result;
                }
            }
        },
        created() {
            axios.get('/api/v1/income/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.income_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
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
            axios.get('api/v1/income/show_income_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/income_history/register_income/',
                    data: {
                        'inc_category': this.inc_category,
                        'fund_category': this.fund_category,
                        'date': this.date,
                        'value': this.value,
                        'comment': this.comment,
                    }
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.$router.go('/Incomes/')
                }).catch(error => {
                    alert(error.response.data)
                })
            },
            clear() {
                this.group = null;
                this.inc_category = null;
                this.fund_category = null;
                this.date = null;
                this.comment = null;
                this.is_shared = null;
            }
        }
    }
</script>
<style scoped>
    .cont {
        height: 100vh;
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }

    .text {
        width: fit-content;
        margin: auto;
    }

    .cont div {
        margin: auto;
        padding-top: 2%;
    }
</style>
