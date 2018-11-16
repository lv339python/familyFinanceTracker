<template>
    <div class="content">
        <div id="left">
            <div v-if="totalList.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'
                    v-bind:deleteItem="delItSpending"
                    v-bind:showModal='showModal'
                    v-if="list.length !== 0"/>
            </div>
            <b-modal ref="myModalRef" hide-footer title='Spending'>
                <div class="d-block text-center">
                    <b-card>
                        <p class="card-text">
                            <b v-if="modalData['icon']">
                            <img class='image' :src="modalData['icon']"> <br></b>
                            <b>Name: {{modalData['name']}}</b>
                            <br>
                            <b>Total spend for this category: {{modalData['total']}}</b>
                            <br>
                            <b v-if="modalData['last_value']"> Last spend registered:
                                {{modalData['last_value']}} on {{modalData['last_date']}}<br></b>
                            <b v-if="modalData['spend_group']">Spending is shared from
                                {{modalData['spend_group']}} group <br></b>
                            <br>
                        </p>
                        <b-btn class="mt-3" variant="outline-danger" @click="hideModal">Cancel</b-btn>
                    </b-card>
                </div>

            </b-modal>

        </div>

        <div id="right">
            <b-button-group size="lg" class="btn-group">
                <b-button v-b-toggle.collapse1 variant="primary" to="/spendings/limit_ind" >
                    Set Individual Limitation
                </b-button>
                <b-button v-b-toggle.collapse1 variant="primary" to="/spendings/limit_group" v-if="group_spends">
                    Set Group Limitation
                </b-button>
                <b-button v-b-toggle.collapse1 variant="primary" to="/spendings/history" >History</b-button>
            </b-button-group>
            <b-collapse id="collapse1" class="mt-2">
                <b-card>
                    <router-view></router-view>
                </b-card>
            </b-collapse>
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
                group_spends: false,
                modalData: {}
            }
        },
        methods: {
            showModal(data) {
                this.$refs.myModalRef.show();
                this.getModalData(data)
            },
            hideModal() {
                this.$refs.myModalRef.hide()
            },
            getModalData: function (data) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/summary/',
                    data: {
                        'spend_id': data,
                    }
                }).then(response => {
                    this.modalData = response.data;
                }).catch(error => {
                    alert(error.response.data)
                })
            },
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
        display: flex;
        flex-direction: row;
        justify-content: space-evenly;
    }

    #left {
        flex-shrink: 0;
        background-color: whitesmoke;
        margin: 5px;
        padding: 5px;
        width: 25%;
    }

    #right {
        background-color: #f3f3f3;
        padding: 5px;
        margin: 0;
        width: 100%;
        display: flex;
        flex-direction: column;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
    .btn-group{
        height: fit-content;
        margin: 0 auto;
    }

    .image {
        width: 15%;
        height: 15%;
    }
</style>
