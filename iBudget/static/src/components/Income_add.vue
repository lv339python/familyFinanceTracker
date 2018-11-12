<template>
    <div id="income_add">
        <div>
            <hr>
            <div class="form-group">
                <label for="name">Name of income:</label>
                <input v-model="newName" placeholder="Name" id="name">
            </div>
        </div>

        <div>
            <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
        </div>

        <div>
            <div>
                <label>Select date</label>
                <input v-model="incomeDate" type="date">
                <hr>
            </div>
        </div>


        <div>
            <label for="value">Value:</label>
            <br>
            <input v-model.number="incomeValue" id="value"
                   type="number" min="0" max="999999999"
                   placeholder="Value">
        </div>


        <div v-show="isValidData">
            <hr>
            <button class="btn btn-outline-primary" v-on:click="createIncome" :variant="secondary">Create income
            </button>
            <button v-on:click="createDone" :variant="secondary" v-show="isDone">{{msg}}</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Icon_getter from './Icon_getter';


    export default {
        name: "Income_add",
        props: ["tabName"],
        components: {'icon_getter': Icon_getter},
        data() {
            return {
                isDone: false,
                newName: null,
                incomeDate: null,
                incomeValue: null,
                selectedIcon: '',
                newIncome: {
                    'name': null,
                    'icon': '',
                    'date': null,
                    'value': null
                },
                msg: '',
                tab: 'income'

            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result = (this.newName != null && this.incomeDate != null && this.incomeValue != null);
                    return result;
                }
            }
        },
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            },
            createIncome: function (event) {
                console.log(this.newName,
                    this.selectedIcon,
                    this.incomeDate,
                    this.incomeValue);
                axios({
                    method: 'post',
                    url: '/api/v1/income/create_category/',
                    data: {
                        'name': this.newName,
                        'icon': this.selectedIcon,
                        'date': this.incomeDate,
                        'value': this.incomeValue
                    }
                }).then(response => (this.msg = response.data));
                this.isDone = true;
            },
            createDone: function (event) {
                this.$router.go('/income_add')
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            }
        }
    }
</script>

<style scoped>
</style>
