<template>
    <div class="content">
        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Select income category:</label>
                <select v-model="inc_category" class="form-control">
                    <option v-for="income in income_list" v-bind:value="income.id"> {{ income.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Choose your fund:</label>
                <select v-model="fund_category" class="form-control">
                    <option v-for="fund in fund_list" v-bind:value="fund.id"> {{ fund.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Input sum of your income </label>
                <input v-model="value" type="number" min="1" class="form-control">
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Input comment</label>
                <input v-model="comment" type="text" class="form-control">
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Choose date</label>
                <input v-model="date" type="date">
            </div>
            <hr>
        </div>

        <!--<div class="col-md-4">-->
        <!--<hr>-->
        <!--<div class="form-group">-->
        <!--<label>Chose group</label>-->
        <!--<select v-model="group" class="ourform">-->
        <!--<option v-for="group in group_list"-->
        <!--v-bind:value="group.id"-->
        <!--v-on:click="is_active_shared_cat=group.id">-->
        <!--{{ group.name }}-->
        <!--</option>-->
        <!--</select>-->
        <!--</div>-->
        <!--<hr>-->
        <!--</div>-->

        <!--<div class="col-md-4">-->
        <!--<hr>-->
        <!--<div class="form-group">-->
        <!--<label>Chose category</label>-->
        <!--<select v-model="category" class="ourform">-->
        <!--<option v-for="category in shared_list"-->
        <!--v-if="category.id_group === is_active_shared_cat"-->
        <!--v-bind:value="category.id_cat">-->
        <!--{{category.name_cat}}-->
        <!--</option>-->
        <!--</select>-->
        <!--</div>-->
        <!--<hr>-->
        <!--</div>-->

        <!--<input type="checkbox" id="shared_button" v-model="is_shared">-->
        <!--<label for="shared_button">Shared</label>-->
        <!--<span>{{ is_shared }}</span>-->
        <button v-on:click="setData" :variant="secondary">Save</button>
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
                // shared_category: null,
                inc_category: null,
                fund_category: null,
                value: null,
                date: null,
                comment: null,
                is_active_shared_cat: null,
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
            axios.get('api/v1/spending/show_spending_group/')
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
                    this.$router.go('/Incomes/')
                })
            },
        }
    }
</script>
<style scoped>
    .content {
        height: 100vh;
        display: flex;
        flex-direction: column;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
