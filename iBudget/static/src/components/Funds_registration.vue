<template>
    <div id="fund_registration">
        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label>Input name</label>
                <input type="text" v-model="name" class="form-control">
            </div>
            <div>{{ name }}</div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label>Choose icon</label>
                <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
            </div>
        </div>

        <div class="col-md-3">
            <hr>
            <div class="form-group">
                <label>Shared to</label>
                <select v-model="shared_group" class="form-control">
                    <option></option>
                    <option
                        v-for="group in user_groups_list"
                        v-bind:value="group.id">
                        {{ group.name }}
                    </option>
                </select>
            </div>
        </div>
        <hr>
        <div class="col-md-2">
            <button class="btn btn-outline-primary" v-on:click="setData" :variant="secondary">Save</button>
        </div>
        <div>
            <label>Select fund:</label>
            <select v-model="fund_id" class="form-control">
                <option v-for="fund in fund_list" v-bind:value="fund.id">
                    {{ fund.name }}
                </option>
            </select>
        </div>
        <div class="col-md-4">
        <button type="button" class="btn btn-outline-danger" v-on:click="Delete" :variant="secondary">Delete fund
        </button>
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
                shared_group: null,
                icon: null,
                group: null,
                user_groups_list: [],
                tab: 'fund',
                selectedIcon: '',
                fund_id: null,
                fund_list: [],
                is_active: null
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
                });

        axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/fund/create_new_fund/',
                    data: {
                        'name': this.name,
                        'icon': this.selectedIcon,
                        'shared_group': this.shared_group
                    }
                }).then(response => {
                    this.$router.go('/create_new_fund/')
                })
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            },
             Delete: function (event) {
                axios({
                    method: 'put',
                    url: '/api/v1/fund/delete_fund_category/'+ this.fund_id,
                    data: {
                        'is_active': this.is_active
                    }
                }).then(response => {
                    this.$router.go('/spendings/new/')
                })

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
