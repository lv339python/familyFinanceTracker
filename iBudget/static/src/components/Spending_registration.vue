<template>
    <div class="content">
        <div class="row">
            <div class="col-md-8 form-group " v-if="is_shared===true">
                <p>Choose group:</p>
                <div class="img_container">
                    <div v-for="group in group_list">
                        <input type="image" :src="group.url" v-on:click="get_group_icon_id(group.id)"
                               class="icon" alt="icon">
                        <p>{{group.name}}</p>
                    </div>
                </div>
                <hr>
                <div v-show="groupId">
                    <p>Select category:</p>
                    <div class="img_container">
                        <div v-for="category in shared_list" v-if="category.id_group === group_id">
                            <input type="image" :src="category.url"
                            v-on:click="get_spend_icon_id(category.id_cat)"
                                   class="icon" alt="icon">
                            <p>{{category.name_cat}}</p>
                        </div>
                    </div>
                    <hr/>
                    <p>Choose type of pay:</p>
                    <div class="img_container">
                        <div v-for="type_of_pay in shared_fund_list" v-if="type_of_pay.id_group === group_id">
                            <input type="image" :src="type_of_pay.url"
                            v-on:click="get_group_fund_id(type_of_pay.id_fund)"
                                   class="icon" alt="icon">
                            <p>{{type_of_pay.name_fund}}</p>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-md-8 form-group" v-else>
                <p>Select category:</p>
                <div class="img_container">
                    <div v-for="spend in spending_list">
                        <input type="image" :src="spend.url" v-on:click="get_spend_icon_id(spend.id)"
                                alt="icon" class="icon">
                        <p>{{spend.name}}</p>
                    </div>
                </div>
                <hr/>
                <p>Choose type of pay:</p>
                <div class="img_container">
                    <div v-for="fund in fund_list">
                        <input type="image" :src="fund.url" v-on:click="get_fund_icon_id(fund.id)"
                               class="icon" alt="icon">
                        <p>{{fund.name}}</p>
                    </div>
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
                group_id: null
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
                        'group_id':this.group_id
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
            get_spend_icon_id(id){
                this.category = id;
            },
            get_fund_icon_id(id){
                this.type_of_pay = id
            },
            get_group_icon_id(id){
                this.group_id = id;
                this.groupId = true;
            },
            get_group_fund_id(id){
                this.type_of_pay = id
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
        width: 350px;
        max-height:350px;
        overflow:scroll;
        display: flex;
        flex-direction: row;
        flex-wrap:wrap;
    }
    .icon{
        width:70px;
        height:70px;
    }

    div.img_container div{
        width:70px;
        height:95px;
    }
</style>
