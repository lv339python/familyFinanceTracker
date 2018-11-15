<template>
    <div class="content">
        <div id="left" class="text column">
            <!--<b-button :variant="secondary" to="/incomes/tracking" @click="isList=false">Tracking</b-button>-->
            <!--<router-view></router-view>-->
            <div v-if="list.length!==0">
                <list-paginated
                    v-bind:list='list'
                    v-bind:title='title'
                    v-bind:deleteItem="deleteIncome"
                   v-bind:showModal='showModal'
                    v-if="list.length !== 0"/>
            </div>
            <b-collapse ref id="collapse2">
                <b-card>
                    I am collapsable content!
                </b-card>
            </b-collapse>
            <b-modal ref="myModalRef" hide-footer title='Spending'>
                <div class="d-block text-center">
                    <b-card>
                        <p class="card-text">
                            <b>Name: {{modalData['name']}}</b>
                            <br>
                            <b v-if="modalData['icon']">Icon:
                                 <img class='image' :src="modalData['icon']"> <br></b>
                            <b>Total value for this category: {{modalData['total']}}</b>
                            <br>
                            <b v-if="modalData['last_value']"> Last income registered:
                                {{modalData['last_value']}} on {{modalData['last_date']}}</b>
                            <br>
                        </p>
                        <b-btn class="mt-3" variant="outline-danger" @click="hideModal">Cancel</b-btn>
                    </b-card>
                </div>
            </b-modal>

        </div>
        <div id="right" class="column">
            <income-tracker></income-tracker>
        </div>
    </div>

</template>

<script>
    import axios from 'axios';
    import List_paginated from '../components/List_paginated';
    import Income_tracker from '../components/Income_tracker'

    export default {
        components: {'list-paginated': List_paginated, 'income-tracker' : Income_tracker},
        data() {
            return {
                list: [],
                title: "Incomes",
                errors: [],
                id: 0,
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
                    url: '/api/v1/income/summary/',
                    data: {
                        'income_id': data,
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
                url: '/api/v1/income/'
            })
                .then(response => {
                    this.list = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                });
            },
            deleteIncome(incId) {
                if (incId) {
                    axios({
                        method: 'delete',
                        url: '/api/v1/income/delete_income/' + incId,
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
        /*margin: 5px;*/
        padding: 5px;
        width: 25%;
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
