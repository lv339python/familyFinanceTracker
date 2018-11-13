<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/spendings/add" @click="isList=false">Add</b-button>
            <b-button :variant="secondary" to="/spendings/limit_ind" @click="isList=false">Set Individual Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/limit_group" @click="isList=false" v-if="group_spends">Set Group Limitation</b-button>
            <b-button :variant="secondary" to="/spendings/history" @click="isList=false">History</b-button>
            <b-button :variant="secondary" to="/spendings/new" @click="isList=false">New</b-button>
        </div>
        <div id="right" class="column">
            <div v-if="isList&& list.length!==0&&list_shared.length!==0&&totalList.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title' v-if="list.length !== 0"
                    v-bind:showModal='showModal'/>
            </div>
            <b-modal ref="myModalRef" hide-footer title="Account">
                <div class="d-block text-center">
                    <b-card>
                        <p class="card-text">
                            <b>Name: </b> {{reply['name']}}
                            <br>
                            <b v-if="reply['icon']">Icon: {{reply['icon']}} </b>
                            <br>
                            <!--<img id="profile-photo" rounded="circle" blank width="75" height="75"-->
                            <!--blank-color="orange" alt="img" class="m-1"-->
                            <!--src="http://cdn.onlinewebfonts.com/svg/img_191958.png"/>-->
                            <b>Total spend for this category: </b> {{reply['total_spend']}}
                            <br>
                            <b v-if="reply['last_spend_value']"> Last spend for this category:
                                {{reply['last_spend_value']}} on {{reply['last_spend_date']}}</b>
                            <br>
                            <b v-if="reply['spend_group']">Spending is shared from
                                {{reply['spend_group']}} group </b>
                        </p>
                        <b-btn class="mt-3" variant="outline-danger" @click="hideModal">Log Out</b-btn>
                    </b-card>
                </div>

            </b-modal>
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
                group_spends: false,
                kilka: null,
                reply: {}
            }
        },
        methods: {
            showModal(data) {
                this.$refs.myModalRef.show();
                this.kilka = data;
                this.getData(data)
            },
            hideModal() {
                this.$refs.myModalRef.hide()
            },
            getData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending/summary/',
                    data: {
                        'spend_id': event,
                    }
                }).then(response => {
                    this.reply = response.data;
                    return this.reply
                }).catch(error => {
                    alert(error.response.data)
                })
            },
        },
            created() {
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
                    if(response.data.length > 0){
                        this.group_spends = true
                    }
                })
                .catch(e => {
                    this.errors.push(e)
                });
        },
        computed: {
            totalList: function () {
                if (this.list_shared.length != 0) {
                    let result = this.list;
                    for (var i = 0; i < this.list_shared.length; i++) {
                        result.push({
                            'id': this.list_shared[i].id_cat,
                            'name': this.list_shared[i].name_cat + ' / ' + this.list_shared[i].name_group});
                    };
                    return result
                }
            },
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
