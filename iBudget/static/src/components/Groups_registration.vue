<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Create new group
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Create new group">
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                        <div class="form-group">
                            <label>Input name</label>
                            <input type="text" v-model="name" class="form-control">
                        </div>
                        <br/>
                        <div class="form-group">
                            <label>Choose icon</label>
                            <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
                        </div>
                        <br/>
                    </p>
                    <b-btn class="mt-3" variant="outline-primary" block v-on:click="setData">Create</b-btn>
                    <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Close</b-btn>
                </b-card>
            </div>
        </b-modal>
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
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
            },
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
