<template>
    <div id="spending_add">
          <b-button variant="primary" @click="showModal">
            +
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add new spending category">

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

        <div v-show="isValidData" >
            <hr>
            <button class="btn btn-outline-dark" v-on:click="createSpending" :variant="secondary">Create spending
            </button>
            <button class="btn btn-outline-dark" v-on:click="createDone" :variant="secondary" v-show="isDone">{{msg}}
            </button>
        </div>
      </b-modal>
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
                tab: 'spending'

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
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            },
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
            }
        }
    }
</script>

<style scoped>
</style>
