<template>
    <div id="Groups_registration">
        <div class="col-md-4">
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
            <button class="btn btn-outline-primary" v-on:click="setData" :variant="secondary">Create</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Icon_getter from './Icon_getter.vue';

    export default {
        name: "Groups_registration",
        data() {
            return {
                name: null,
                icon: null,
                tab: 'group',
                selectedIcon: ''
            }
        },
        components: {
            'Icon_getter': Icon_getter
        },
        props: ["tabName"],
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/group/create_new_group/',
                    data: {
                        'name': this.name,
                        'icon': this.selectedIcon
                    }
                }).then(response => {
                    this.$router.go('/group_registration/')
                })
            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            }
        },
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
