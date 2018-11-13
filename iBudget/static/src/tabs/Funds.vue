<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/funds/tracking_goal" @click="isList=false">Tracking Goal</b-button>
            <b-button :variant="secondary" to="/funds/new_goal" @click="isList=false">New Goal</b-button>
            <b-button :variant="secondary" to="/funds/new" @click="isList=false">New Fund</b-button>
        </div>
         <div  id="right" class="column">
            <div v-if="isList&& totalList.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'  v-if="list.length !== 0"
                    v-bind:showModal='showModal'/>
            </div>
             <b-modal ref="myModalRef" hide-footer title="Fund">
                 <div class="d-block text-center">
                     <b-card>
                             <b>Name: {{modalData['name']}}</b>
                             <br>
                             <b v-if="modalData['icon']">Icon:
                                 <img class='image' :src="modalData['icon']"> <br></b>
                             <b v-if="modalData['spend_group']">Shared is shared from
                                 {{modalData['spend_group']}} group <br></b>
                             <b>Current balance for fund: {{modalData['total']}}</b>
                             <br>
                             <b v-if="modalData['last_inc_value']"> Last income for fund:
                                 {{modalData['last_inc_value']}} on {{modalData['last_inc_date']}} <br></b>
                             <b v-if="modalData['last_spend_value']"> Last spend for fund:
                                 {{modalData['last_spend_value']}} on {{modalData['last_spend_date']}}</b>
                         <b-btn class="mt-3" variant="outline-danger" @click="hideModal">Cancel</b-btn>
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
                list_ind:[],
                list_shared:[],
                list: [],
                title: "Funds",
                errors: [],
                modalData: {}
            }
        },
        methods: {
            showModal(data) {
                this.$refs.myModalRef.show();
                this.getData(data)
            },
            hideModal() {
                this.$refs.myModalRef.hide()
            },
            getData: function (data) {
                axios({
                    method: 'post',
                    url: '/api/v1/fund/summary/',
                    data: {
                        'fund_id': data,
                    }
                }).then(response => {
                    this.modalData = response.data;
                }).catch(error => {
                    alert(error.response.data)
                })
            },
        },
        created() {
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
        },
        computed: {
            totalList: function () {
                if (this.list_shared.length != 0) {
                    let result = this.list;
                    for (var i = 0; i < this.list_shared.length; i++) {
                        result.push({
                            'id': this.list_shared[i].id_fund,
                            'name': this.list_shared[i].name_fund + ' / ' + this.list_shared[i].group_name});
                    };
                    return result
                }
            }
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
