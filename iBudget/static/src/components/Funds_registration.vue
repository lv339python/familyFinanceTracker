<template>
    <div id="fund_registration">
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label>Input name</label>
                <input type="text" v-model="name" class="form-control">
            </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Choose icon</label>
                <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
            </div>
        </div>
        <hr>
        <div class="col-md-2">
            <button class="btn btn-outline-primary" v-on:click="setData" :variant="secondary">Save</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Icon_getter from './Icon_getter.vue'

    export default {
        name: "fund_registration",
        data() {
            return {
                name: null,
                icon: null,
                group: null,
                user_groups_list: [],
                tab: 'fund',
                selectedIcon: ''
            }
        },
        props: ["tabName"],
        components: {
            'Icon_getter': Icon_getter
        },
        created() {
            axios.get('/api/v1/group/show_users_group/')
                .then(response => {
                    this.user_groups_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/fund/create_new_fund/',
                    data: {
                        'name': this.name,
                        'icon': this.selectedIcon
                    }
                }).then(response => {
                    this.$router.go('/create_new_fund/')
                })
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            }
        }
    }
</script>

<style scoped>
    .content {
        height: 100vh;
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
