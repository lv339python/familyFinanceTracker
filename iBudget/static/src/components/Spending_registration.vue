<template>
    <div class="content">
        <div class="col-md-4 group" v-if="is_shared===true">
            <div class="form-group ">
                <label>Chose group</label>
                <select v-model="group" class="form-control">
                    <option v-for="group in group_list"
                            v-bind:value="group.id"
                            v-on:click="is_active_shared_cat=group.id">
                        {{ group.name }}
                    </option>
                </select>
                <hr>
            </div>

            <div class="form-group" v-show="isSharedSpending">
                <label>Select category</label>
                <select v-model="category" class="form-control">
                    <option v-for="category in shared_list"
                            v-if="category.id_group === is_active_shared_cat"
                            v-bind:value="category.id_cat">
                        {{category.name_cat}}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4 group" v-else>
            <div class="form-group">
                <label>Select category:</label>
                <select v-model="category" class="form-control">
                    <option v-for="spend in spending_list" v-bind:value="spend.id ">
                        {{ spend.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="center">
            <input type="checkbox" id="cbx" style="display:none" v-model="is_shared"/>
            <label for="cbx" class="toggle"><span></span>Shared</label>
        </div>

        <div class="col-md-4">
            <div class="form-group" id="type_of_pay">
                <label>Choose type of pay:</label>
                <select v-model="type_of_pay" class="form-control">
                    <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id">
                        {{ type_of_pay.name }}
                    </option>
                </select>
            </div>
        </div>

        <div class="col-md-4">
            <div class="form-group" id="sum">
                <label>Input sum:</label>
                <input v-model="value" type="number" min="1" class="form-control">
            </div>
        </div>

        <div class="col-md-4">
            <div class="form-group" id="comment">
                <label>Input comment:</label>
                <input v-model="comment" type="text" class="form-control">
            </div>
        </div>

        <div class="col-md-4" id="date">
            <label>Choose date:</label>
            <div class="form-group">
                <input v-model="date" type="date">
            </div>
        </div>

        <div id="reset">
            <button type="button" class="btn btn-outline-danger" @click="reset">Reset</button>
        </div>

        <div id="save" v-show="isValidData">
            <button type="button" class="btn btn-outline-primary" @click="setData" :variant="secondary">Save</button>
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
                group: null,
                category: null,
                type_of_pay: null,
                value: null,
                date: null,
                comment: null,
                is_active_shared_cat: null,
                is_shared: null,
                tax: '',
            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.category != null &&
                        this.type_of_pay != null &&
                        this.value != null &&
                        this.date != null &&
                        this.comment != null;
                    return result;
                }
            },
            isSharedSpending: {
                get: function () {
                    var result =
                        this.group = this.is_active_shared_cat;
                    return result
                }
            }
        },
        created() {
            axios.get('/api/v1/spending/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.spending_list = response.data
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
                    }
                }).then(response => {
                    this.$router.go('/Spendings/')
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
        margin: 20px;
    }
    #type_of_pay {
        position: relative;
        left: 20px;
        top: -50px;
    }
    #sum{
        position: relative;
        top: 20px;
    }
    #comment{
        position: relative;
        top: 20px;
    }
    #date{
        position: relative;
        top: -150px;
        left: -815px;
    }
    #reset{
        position: absolute;
        right: 435px;
        top: 616px;

    }
    #save{
        position: absolute;
        right: 370px;
        top: 616px;

    }
    .toggle {
        position: absolute;
        left: 710px;
        top: 120px;
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
