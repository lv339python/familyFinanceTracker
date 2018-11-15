<template>

    <div class="content">
        <b-button class="btn btn-warning btn-circle btn-xl" @click="showModal" data-toggle="tooltip" title="Create Goal">
            ✰
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Create Goal">

            <div class="form-group">
                <div>

                    <input type="text" placeholder="Input name" v-model="name" class="form-control">
                </div>
            </div>
            <div class="form-group">
                <div>
                    <input v-model="value" placeholder="Input value" type="number" min="1" class="form-control">
                </div>
            </div>

            <div class="form-group">
                <div>
                    <label>Choose icon</label>
                    <icon_getter @get_name='onGet_name' :tabName="tab"></icon_getter>
                </div>
            </div>

            <div class="form-group">
                <div>
                    <label>Shared to</label>
                    <select v-model="shared_group" class="form-control">
                        <option
                            v-for="group in user_groups_list"
                            v-bind:value="group.id">
                            {{ group.name }}
                        </option>
                    </select>
                </div>
            </div>

            <div>

                <div class="form-group">
                    <label>Start Date</label>
                    <input placeholder="Start Date" v-model="start_date" type="date">
                    <label>Finish Date</label>
                    <input v-model="finish_date" placeholder="Finish Date" type="date">
                </div>
            </div>

            <div>
                <div class="form-group">

                </div>
            </div>

            <div>
                <button type="button" class="btn btn-outline-danger" @click="reset">Reset</button>
                <button :disabled="isValidData===false" type="button" class="btn btn-outline-primary" @click="setData"
                        :variant="secondary">Save
                </button>
            </div>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';
    import Icon_getter from './Icon_getter.vue'

    export default {
        name: "Financial_goal",
        data() {
            return {
                start_date:  new Date().toJSON().slice(0, 10),
                finish_date:  new Date().toJSON().slice(0, 10),
                value: null,
                name: null,
                shared_group: null,
                icon: null,
                group: null,
                user_groups_list: [],
                tab: 'fund',
                selectedIcon: ''
            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.start_date != null &&
                        this.finish_date != null &&
                        this.value != null &&
                        this.name != null;
                    return result;
                }
            },
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
                    url: '/api/v1/fund/create_new_goal/',
                    data: {
                        'value': this.value,
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'fund': this.fund,
                        'name': this.name,
                        'icon': this.selectedIcon,
                        'shared_group': this.shared_group
                    }
                }).then(response => {
                    this.$router.go('fund/')
                })

            },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            },
            reset() {
                this.shared_group = null;
                this.start_date = new Date().toJSON().slice(0, 10);
                this.finish_date = new Date().toJSON().slice(0, 10);
                this.value = null;
                this.name = null;
                this.icon = null;

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
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
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
