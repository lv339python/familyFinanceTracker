<template>
    <div class="content">
        <div class="row">
            <div class="col-md-8 form-group " v-if="is_shared===true">
                <!--<div>-->
                    <!--<label>Choose group</label>-->
                    <!--<select v-model="groupId" class="form-control">-->
                        <!--<option v-for="group in group_list"-->
                                <!--v-bind:value="group.id">-->
                            <!--{{ group.name }}-->
                        <!--</option>-->
                    <!--</select>-->
                <!--</div>-->
                <p>Choose group:</p>
                <div class="img_container">
                    <br>
                    <template v-for="group in group_list">
                        <input type="image" :src="group.url" v-on:click="get_group_icon_id(group.id)"
                               class="icon" alt="no icon"> {{group.name}}
                    </template>
                </div>
                <hr>
                <div v-show="groupId">
                    <label>Select category</label>
                    <select v-model="category" class="form-control">
                        <option v-for="category in shared_list"
                                v-if="category.id_group === groupId"
                                v-bind:value="category.id_cat">
                            {{category.name_cat}}
                        </option>
                    </select>
                    <hr/>
                    <label>Choose type of pay:</label>
                    <select v-model="type_of_pay" class="form-control">
                        <option v-for="type_of_pay in shared_fund_list"
                                v-if="type_of_pay.id_group===groupId"
                                v-bind:value="type_of_pay.id_fund">
                            {{ type_of_pay.name_fund }}
                        </option>
                    </select>
                </div>
            </div>

            <div class="col-md-8 form-group" v-else>
                <p>Select category:</p>
                <div class="img_container">
                    <br>
                    <template v-for="spend in spending_list">
                        <input type="image" :src="spend.url" v-on:click="get_spend_icon_id(spend.id)"
                               class="icon"> {{spend.name}}
                    </template>
                </div>
                <hr/>
                <p>Choose type of pay:</p>
                <div class="img_container">
                    <br>
                    <template v-for="fund in fund_list">
                        <input type="image" :src="fund.url" v-on:click="get_fund_icon_id(fund.id)
                               class="icon"> {{fund.name}}
                    </template>
                </div>
            </div>

            <div class="col-md-4">
                <input type="checkbox" id="cbx" style="display:none" v-model="is_shared"/>
                <label for="cbx" class="toggle"><span></span>Shared</label>
            </div>
        </div>

        <div class="col-md-4 form-group">
            <label>Input sum:</label>
            <input v-model="value" type="number" min="1" class="form-control">
        </div>

        <div class="col-md-4 form-group">
            <label>Input comment:</label>
            <input v-model="comment" type="text" class="form-control">
        </div>

        <div class="col-md-4">
            <label>Choose date:</label>
            <div class="form-group">
                <input v-model="date" type="date">
            </div>
        </div>

        <div>
            <button type="button" class="btn btn-outline-danger" @click="reset">Reset</button>
            <button :disabled="isValidData===false" type="button" class="btn btn-outline-primary" @click="setData"
                    :variant="secondary">Save
            </button>
        </div>
    </div>
</template>


<script>
    import axios from 'axios';

    export default {
        name: "spending_history",
        data() {
            return {
                spending_list: [],
                fund_list: [],
                group_list: [],
                shared_list: [],
                shared_fund_list: [],
                groupId: null,
                category: null,
                type_of_pay: null,
                value: null,
                date: new Date().toJSON().slice(0,10),
                comment: null,
                is_shared: false,
            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.category != null &&
                        this.type_of_pay != null &&
                        this.value != null &&
                        this.date != null;
                    return result;
                }
            }
        },
        created() {
            axios.get('/api/v1/spending/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.spending_list = response.data.categories
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
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
            axios.get('api/v1/spending/show_spending_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('api/v1/fund/show_fund_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending_history/register_spending/',
                    data: {
                        'category': this.category,
                        'type_of_pay': this.type_of_pay,
                        'date': this.date,
                        'value': this.value,
                        'comment': this.comment,
                        'group_id':this.groupId
                    }
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.$router.go('/spendings/add/')
                }).catch(error => {
                    alert(error.response.data)
                })
            },
            reset() {
                this.group = null;
                this.type_of_pay = null;
                this.value = null;
                this.date = null;
                this.comment = null;
                this.category = null;
                this.is_active_shared_cat = null;
                this.is_shared = false;
            },
            get_spend_icon_id(icon_name){
                this.category = icon_name;
            },
            get_fund_icon_id(icon_name){
                this.type_of_pay = icon_name
            },
            get_group_icon_id(icon_name){
                this.group_id = icon_name
            }
        }
    }
</script>

<style scoped>
    .content {
        height: 100vh;
        display: flex;
        flex-direction: column;
        flex-wrap: wrap;
    }
    .row {
        margin: 0;
    }
    .toggle {
        margin: 4vh;
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
    .img_container{
        width: 380px;
        height: 380px;
        display: flex;
        flex-direction: column;
        flex-wrap:wrap;
    }
    .icon{
        width:70px;
        height:70px;
    }
</style>
