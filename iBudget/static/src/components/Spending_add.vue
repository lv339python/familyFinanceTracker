<template>
    <div id="spending_add">

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label for="name">Name of spending:</label>
                <input v-model="newName" placeholder="Name" id="name">
            </div>
        </div>

        <div class="col-md-4">
            <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
        </div>

        <div v-show="isValidData" class="col-md-4">
            <hr>
            <button class="btn btn-outline-dark" v-on:click="createSpending" :variant="secondary">Create spending
            </button>
            <button class="btn btn-outline-dark" v-on:click="createDone" :variant="secondary" v-show="isDone">{{msg}}
            </button>
        </div>





        <div>
            <label>Select category:</label>
            <select v-model="spending_id" class="form-control">
                <option v-for="spend in spending_list" v-bind:value="spend.id">
                    {{ spend.name }}
                </option>
            </select>
        </div>

        <div class="col-md-4">
        <button type="button" class="btn btn-outline-danger" v-on:click="Delete" :variant="secondary">Delete spending
        </button>
        </div>





    </div>
</template>

<script>
    import axios from 'axios';
    import Icon_getter from './Icon_getter';


    export default {
        name: "Spending_add",
        props: ["tabName"],
        components: {'icon_getter': Icon_getter},
        data() {
            return {
                isDone: false,
                newName: null,
                selectedIcon: '',
                newSpending: {
                    'name': null,
                    'icon': ''
                },
                msg: '',



                tab: 'spending',
                is_active: null,
                spending_list: [],
                spending_id: null



            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result = (this.newName != null);
                    return result;
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
        },




        methods: {
            createSpending: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/add/',
                    data: {
                        'name': this.newName,
                        'icon': this.selectedIcon
                    }
                }).then(response => (this.msg = response.data));
                this.isDone = true;
            },
            createDone: function (event) {
                this.$router.go('/spending_add')
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            },




            Delete: function (event) {
                axios({
                    method: 'delete',
                    url: '/api/v1/spending/delete_spending_category/'+ this.spending_id,
                }).then(response => {
                    this.$router.go('/spendings/new/')
                })

            }


        }
    }
</script>

<style scoped>
</style>
