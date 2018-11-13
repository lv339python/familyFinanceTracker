<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/funds/tracking_goal" @click="isList=false">Tracking Goal</b-button>
            <b-button :variant="secondary" to="/funds/new_goal" @click="isList=false">New Goal</b-button>
            <b-button :variant="secondary" to="/funds/new" @click="isList=false">New Fund</b-button>
        </div>
        <div id="right" class="column">
            <div v-if="isList&&totalList.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'
                    v-bind:deleteItem="delItFundGoal"
                    v-if="list.length !== 0"/>
            </div>
            <div v-if="isList&&totalListGoal.length!==0">
                <list_paginated
                    v-bind:list='listGoal'
                    v-bind:title='titleGoal'
                    v-bind:deleteItem="delItFundGoal"
                    v-if="list.length !== 0"/>
            </div>
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import List_paginated from '../components/List_paginated';

    export default {
        name: "Funds",
        components: {'List_paginated': List_paginated},
        data() {
            return {
                isList: true,
                list_shared: [],
                list_sharedGoal: [],
                listGoal: [],
                list: [],
                title: "Funds",
                titleGoal: "Financial Goal",
                errors: [],
                fund_id: null,
                id: 0
            }
        },
        computed: {
            totalList: function () {
                {
                    let result = this.list;
                    for (var i = 0; i < this.list_shared.length; i++) {
                        result.push({
                            'id': this.list_shared[i].id_fund,
                            'name': this.list_shared[i].name_fund + ' / ' + this.list_shared[i].group_name
                        });
                    }
                    return result
                }
            },
            totalListGoal: function () {
                {
                    let result = this.listGoal;
                    for (var i = 0; i < this.list_sharedGoal.length; i++) {
                        result.push({
                            'id': this.list_sharedGoal[i].id_fund,
                            'name': this.list_sharedGoal[i].name_fund + ' / ' + this.list_sharedGoal[i].group_name
                        });
                    }
                    ;
                    return result
                }
            }
        },
        methods: {
            getData() {
                axios({
                    method: 'get',
                    url: '/api/v1/fund/'
                })
                    .then(response => {
                        this.list = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios({
                    method: 'get',
                    url: '/api/v1/income/show_income_group/'
                })
                    .then(response => {
                        this.list_shared = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios({
                    method: 'get',
                    url: '/api/v1/fund/show_goal/'
                })
                    .then(response => {
                        this.listGoal = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios({
                    method: 'get',
                    url: '/api/v1/fund/show_goal_by_group/'
                })
                    .then(response => {
                        this.list_sharedGoal = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
            },
            delItFundGoal(fundId) {
                axios({
                    method: 'delete',
                    url: '/api/v1/fund/delete_fund_goal_category/' + fundId,
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.getData();
                }).catch(error => {
                    alert(error.response.data)
                })
            }
        },
        created() {
            this.getData();
        }
    }


</script>

<style scoped>
    .content {
        height: 100%;
        overflow: hidden;
        margin: 0px;
        display: flex;
    }

    .column {
        height: 100%;
        display: flex;
        flex-direction: column;
    }

    #left {
        flex-shrink: 0;
        background-color: whitesmoke;
        margin: 5px;
        padding: 5px;
        width: 16%;
    }

    #right {
        background-color: #f3f3f3;
        padding: 5px;
        margin: 0;
        width: 100%;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
