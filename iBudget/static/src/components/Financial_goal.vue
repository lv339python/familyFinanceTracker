<template>
    <div class="content">
        <div class="col-md-4 group" v-if="is_shared===true">
            <div class="form-group ">
                <label>Chose group</label>
                <select v-model="group" class="form-control">
                    <option v-for="group in group_list"
                            v-bind:value="group.id"
                            v-on:click="is_active_shared_fund=group.id">
                        {{ group.name }}
                    </option>
                </select>
                <hr>
            </div>

            <div class="form-group" v-show="isSharedFund">
                <label>Chose your group goal</label>
                <select v-model="fund" class="form-control">
                    <option v-for="fund in fund_list"
                            v-if="fund.id_group === is_active_shared_fund"
                            v-bind:value="fund.id_fund">
                        {{fund.name_fund}}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4 group" v-else>
            <div class="form-group">
                <label>Chose your goal:</label>
                <select v-model="fund" class="form-control">
                    <option v-for="fund in fund_list_ind" v-bind:value="fund.id"> {{ fund.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="center">
            <input type="checkbox" id="cbx" style="display:none" v-model="is_shared"/>
            <label for="cbx" class="toggle"><span></span>Shared</label>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group" id="value">
                <label>Input value</label>
                <input v-model="value" type="number" min="1" class="form-control">
            </div>
        </div>

        <div class="col-md-4" id="start_date">
            <label>Start date</label>
            <div class="form-group">

                <input v-model="start_date" type="date">
            </div>
            <hr>
        </div>

        <div class="col-md-4" id="finish_date">
            <label>Finish date</label>
            <div class="form-group">

                <input v-model="finish_date" type="date">
            </div>
            <hr>
        </div>


        <div id="reset">
            <button @click="reset">Reset</button>
        </div>

        <div id="save" v-show="isValidData" >
            <button v-on:click="setData" :variant="secondary">Save</button>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Financial_goal",
        data() {
            return {
                fund_list: [],
                fund_list_ind: [],
                group: null,
                group_list: null,
                fund: null,
                start_date: null,
                finish_date: null,
                value: null,
                is_active_shared_fund: null,
                is_shared: null,
                tax: '',
            }
        },

        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.fund != null &&
                        this.start_date != null &&
                        this.finish_date != null &&
                        this.value != null &&
                        this.start_date < this.finish_date;
                    return result;
                }
            },
            isSharedFund: {
                get: function () {
                    var result =
                        this.group = this.is_active_shared_fund;
                    return result
                }
            }
        },


        created() {
            axios.get('/api/v1/fund/users_shared_fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list_ind = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/group/get_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.group_list = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                });
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/fund/register_financial_goal/',
                    data: {
                        'value': this.value,
                        'start_date': this.start_date,
                        'finish_date': this.finish_date,
                        'fund': this.fund
                    }
                }).then(response => {
                    this.$router.go('fund/register_financial_goal')
                })
            },
            reset() {
                this.group = null;
                this.fund = null;
                this.value = null;
                this.start_date = null;
                this.finish_date = null;
                this.is_active_shared_fund = null;
            }
        }
    }
</script>

<style scoped>
    .content {
        height: 40vh;
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }

    .text {
        width: fit-content;
        margin: auto;
    }

    .group {
        margin: 50px;
    }

    #value {
        position: relative;
        left: 50px;
        top: -150px;
    }

    #start_date {
        position: relative;
        top: 50px;
        left: 10px;
    }

    #finish_date {
        position: relative;
        top: 9px;
        left: 10px;
    }

    #reset {
        position: relative;
        left: 483px;
        top: 2px;
        width: 60px;
        background: rgba(82, 220, 69, 0.67);
    }

    #save{
        position: absolute;
        right: 385px;
        top: 729px;
        width: 55px;
        background: rgba(174, 23, 220, 0.67);
    }

    .toggle {
        position: absolute;
        left: 740px;
        top: 145px;
        display: block;
        width: 40px;
        height: 20px;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
        transform: translate3d(0, 0, 0);
    }

    .toggle:before {
        content: "";
        position: relative;
        top: 3px;
        left: 3px;
        width: 34px;
        height: 14px;
        display: block;
        background: #9A9999;
        border-radius: 8px;
        transition: background 0.2s ease;
    }

    .toggle span {
        position: absolute;
        top: 0;
        left: 0;
        width: 20px;
        height: 20px;
        display: block;
        background: white;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(154, 153, 153, 0.5);
        transition: all 0.2s ease;
    }

    .toggle span:before {
        content: "";
        position: absolute;
        display: block;
        margin: -18px;
        width: 56px;
        height: 56px;
        background: rgba(79, 46, 220, 0.5);
        border-radius: 50%;
        transform: scale(0);
        opacity: 1;
        pointer-events: none;
    }

    #cbx:checked + .toggle:before {
        background: #947ADA;
    }

    #cbx:checked + .toggle span {
        background: #4F2EDC;
        transform: translateX(20px);
        transition: all 0.2s cubic-bezier(0.8, 0.4, 0.3, 1.25), background 0.15s ease;
        box-shadow: 0 3px 8px rgba(79, 46, 220, 0.2);
    }

    #cbx:checked + .toggle span:before {
        transform: scale(1);
        opacity: 0;
        transition: all 0.4s ease;
    }


</style>
