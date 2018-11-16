<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Create New Group
        </b-button>
        <b-modal ref="myModalRef4" hide-footer title="Create new group">
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                    <div class="form-group">
                        <label>Input Name</label>
                        <input type="text" v-model="name" class="form-control">
                    </div>
                    <br/>
                    <div class="form-group">
                        <label>Choose Icon</label>
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
        props: ["tabName", "getData"],
        methods: {
            showModal() {
                this.$refs.myModalRef4.show();
            },
            hideModal() {
                this.$refs.myModalRef4.hide();
                this.clearAll();
            },
            clearAll() {
                this.name = null;
                this.icon = null;
            },
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/group/create_new_group/',
                    data: {
                        'name': this.name,
                        'icon': this.selectedIcon
                    },
                }).then(response => {
                    this.hideModal();
                    this.getData();
                    this.clearAll();
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
