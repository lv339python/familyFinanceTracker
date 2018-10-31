<template>
    <div class="content">
        <div class="col-md-4 group" v-if="is_shared===true">
            <div class="form-group ">
                <label>Chose group</label>
                <select v-model="group" class="form-control">
                    <option v-for="group in group_list"
                            v-bind:value="group.id"
                            v-on:click="is_active_shared_cat=group.id">
                        {{ group.name }}
                    </option>
                </select>
                <hr>
            </div>

            <div class="form-group" v-show="isSharedSpending">
                <label>Select category</label>
                <select v-model="category" class="form-control">
                    <option v-for="category in shared_list"
                            v-if="category.id_group === is_active_shared_cat"
                            v-bind:value="category.id_cat">
                        {{category.name_cat}}
                    </option>
                </select>
            </div>

            <div class="form-group" v-show="isSharedSpending">
                <label>Choose type of pay:</label>
                <select v-model="type_of_pay" class="form-control">
                    <option v-for="type_of_pay in shared_fund_list"
                            v-if="type_of_pay.id_group===is_active_shared_cat"
                            v-bind:value="type_of_pay.id_fund">
                        {{ type_of_pay.name_fund }}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4 group" v-else>
            <div class="form-group">
                <label>Select category:</label>
                <select v-model="category" class="form-control">
                    <option v-for="spend in spending_list" v-bind:value="spend.id ">
                        {{ spend.name }}
                    </option>
                </select>
            </div>

            <div class="form-group">
                <label>Choose type of pay:</label>
                <select v-model="type_of_pay" class="form-control">
                    <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id">
                        {{ type_of_pay.name }}
                    </option>
                </select>
            </div>
        </div>


    <div class="center">
        <input type="checkbox" id="cbx" style="display:none" v-model="is_shared"/>
        <label for="cbx" class="toggle"><span></span>Shared</label>
    </div>

    <div class="col-md-4">
        <div class="form-group" id="sum">
            <label>Input sum:</label>
            <input v-model="value" type="number" min="1" class="form-control">
        </div>
    </div>

    <div class="col-md-4">
        <div class="form-group" id="comment">
            <label>Input comment:</label>
            <input v-model="comment" type="text" class="form-control">
        </div>
    </div>

    <div class="col-md-4">
        <label>Choose date:</label>
        <div class="form-group">
            <input v-model="date" type="date">
        </div>
    </div>

    <div id="reset">
        <button type="button" class="btn btn-outline-danger" @click="reset">Reset</button>
    </div>

    <div id="save" v-show="isValidData">
        <button type="button" class="btn btn-outline-primary" @click="setData" :variant="secondary">Save</button>
    </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "spending_history",
        data() {
            return {
                spending_list: [],
                fund_list: [],
                group_list: [],
                shared_list: [],
                shared_fund_list: [],
                group: null,
                category: null,
                type_of_pay: null,
                value: null,
                date: null,
                comment: null,
                is_active_shared_cat: null,
                is_shared: null,
                tax: '',
            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.category != null &&
                        this.type_of_pay != null &&
                        this.value != null &&
                        this.date != null &&
                        this.comment != null;
                    return result;
                }
            },
            isSharedSpending: {
                get: function () {
                    var result =
                        this.group = this.is_active_shared_cat;
                    return result
                }
            }
        },
        created() {
            axios.get('/api/v1/spending/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.spending_list = response.data
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
            axios.get('api/v1/spending/show_spending_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('api/v1/fund/show_fund_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending_history/register_spending/',
                    data: {
                        'category': this.category,
                        'type_of_pay': this.type_of_pay,
                        'date': this.date,
                        'value': this.value,
                        'comment': this.comment,
                    }
                }).then(response => {
                    this.$router.go('/Spendings/')
                })
            },
            reset() {
                this.group = null;
                this.type_of_pay = null;
                this.value = null;
                this.date = null;
                this.comment = null;
                this.category = null;
                this.is_active_shared_cat = null;
            }
        }
    }
</script>
<style scoped>


</style>
