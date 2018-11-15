<template>
    <div class="content">
        <b-button class="btn btn-primary btn-circle btn-xl" @click="showModal" data-toggle="tooltip" title="New Fund">
            $
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="New Fund">
            <div>
                <hr>
                <div class="form-group">
                    <input type="text" placeholder="Input name" v-model="name" class="form-control">
                </div>
            </div>

            <div>
                <hr>
                <div class="form-group">
                    <label>Choose icon</label>
                    <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
                </div>
            </div>
            <hr>
            <div>
                <button class="btn btn-outline-primary" v-on:click="setData" :variant="secondary">Save</button>
            </div>
        </b-modal>
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
                icon: '',
                group: null,
                user_groups_list: [],
                tab: 'fund',
                selectedIcon: '',
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
            },
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            },
        }
    }
</script>

<style scoped>
    .content {
        height: fit-content;
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
    .btn-circle.btn-xl {
        width: 70px;
        height: 70px;
        padding: 10px 16px;
        border-radius: 35px;
        font-size: 24px;
        line-height: 1.33;
    }
</style>
