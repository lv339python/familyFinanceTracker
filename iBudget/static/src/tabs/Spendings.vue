<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/spendings/add" @click="isList=false">Add</b-button>
            <b-button :variant="secondary" to="/spendings/limit_ind" @click="isList=false">Set Individual Limitation
            </b-button>
            <b-button :variant="secondary" to="/spendings/limit_group" @click="isList=false" v-if="group_spends">Set
                Group Limitation
            </b-button>
            <b-button :variant="secondary" to="/spendings/history" @click="isList=false">History</b-button>
            <b-button :variant="secondary" to="/spendings/new" @click="isList=false">New</b-button>
        </div>
        <div id="right" class="column">
            <div v-if="isList&&totalList.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'
                    v-bind:deleteItem="delItSpending"
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
        name: "Spendings",
        components: {'List_paginated': List_paginated},
        data() {
            return {
                isList: true,
                list_ind: [],
                list_shared: [],
                list: [],
                title: "Spendings",
                errors: [],
                group_spends: false
            }
        },
        computed: {
            totalList: function () {
                {
                    let result = this.list;
                    for (var i = 0; i < this.list_shared.length; i++) {
                        result.push({
                            'id': this.list_shared[i].id_cat,
                            'name': this.list_shared[i].name_cat + ' / ' + this.list_shared[i].name_group
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
                    url: '/api/v1/spending/'
                })
                    .then(response => {
                        this.list = response.data.categories;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios({
                    method: 'get',
                    url: '/api/v1/spending/show_spending_group/'
                })
                    .then(response => {
                        this.list_shared = response.data;
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
                axios.get('api/v1/spending/admin/limit/')
                    .then(response => {
                        if (response.data.length > 0) {
                            this.group_spends = true
                        }
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });
            },
            delItSpending(spendId) {
                if (spendId) {
                    axios({
                        method: 'delete',
                        url: '/api/v1/spending/delete_spending_category/' + spendId,
                    }).then(response => {
                        this.reply = response.data;
                        alert(this.reply);
                        this.getData();
                    }).catch(error => {
                        alert(error.response.data)
                    })
                }
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
