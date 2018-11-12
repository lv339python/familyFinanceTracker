<template>
    <div id="spending_add">

        <div >
            <hr>
            <div class="form-group">
                <label for="name">Name of spending:</label>
                <input v-model="newName" placeholder="Name" id="name">
            </div>
        </div>

        <div>
            <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
        </div>

        <div>
            <hr>
            <button
                class="btn btn-outline-dark"
                :disabled="isValidData === false"
                v-on:click="createSpending"
                :variant="secondary">Create spending
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
                newName: null,
                selectedIcon: '',
                msg: '',
                tab: 'spending'

            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result = (this.newName != null && this.newName.trim().length != 0);
                    return result;
                }
            }
        },
        methods: {
            createSpending: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/add/',
                    data: {
                        'name': this.newName.trim(),
                        'icon': this.selectedIcon
                    }
                }).then(response => {
                    this.msg = response.data;
                    alert(this.msg);
                    this.createDone();
                });
            },
            createDone: function (event) {
                this.newName = null;
                this.selectedIcon = '';
                this.msg =''
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            }
        }
    }
</script>

<style scoped>
</style>
