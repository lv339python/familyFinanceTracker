<template>
    <div id="spending_add">

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label for="name">Name of spending:</label>
                <input v-model="newName" placeholder="Name" id="name">
            </div>
        </div>

        <div class="col-md-7">
            <icon_getter @get_name='onGet_name'> </icon_getter>
        </div>

        <div v-show="isValidData">
            <hr>
            <button v-on:click="createSpending" :variant="secondary" >Create spending</button>
            <button v-on:click="createDone" :variant="secondary" v-show="isDone">{{msg}}</button>
        </div>

    </div>
</template>

<script>
import axios from 'axios';
import Icon_getter from './Icon_getter';



export default {
    name: "Spending_add",
    components:{'icon_getter': Icon_getter},
    data () {
        return {
            isDone: false,
            newName: null,
            selectedIcon: '',
            newSpending: {
                'name': null,
                'icon': ''
            },
            msg:''

        }
    },
    computed: {
        isValidData: {
            get: function(){
                var result = (this.newName !=null);
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
                    'name': this.newName,
                    'icon': this.selectedIcon
                }
            }).then(response =>(this.msg = response.data));
            this.isDone=true;
        },
        createDone: function (event) {
            this.$router.go('/spending_add')
        },
        onGet_name (data) {
            this.selectedIcon = data['icon_name']
        }
    }
}
</script>

<style scoped>
</style>
