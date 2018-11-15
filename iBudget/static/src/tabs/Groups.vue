<template>
    <div class="content">
        <div  id="left" class="text column">
            <create_new_group v-bind:getData="getData"></create_new_group>
            <p>There are your groups: {{ users_group_list.length }}</p>
            <ul class="list-group">
                <li
                    class="list-group-item list-group-item-action pointer"
                    v-for="(item, index) in paginatedData"
                    v-on:click="selected_group(index, item.id)"
                    :class="{'active': selected_group_index===index}">
                    <b> name </b>: <i> {{ item.group_name }} </i> <br>
                    <b>your role </b>: <i> {{ item.user_role }} </i> <br>
                    <b>count of users </b>: <i> {{ item.count }} </i>
                    <b-btn
                        class="btn btn-outline-light"
                        variant="outline-primary"
                        block
                        v-if="item.user_role==='Owner' || item.user_role==='Admin'"
                        @click="deleteGroup(item.id)"
                        >Delete group
                    </b-btn>
                </li>
            </ul>
            <div v-show="pageCount>1" class='prevNext'>
                <b style="word-space:2em">&nbsp;</b>
                <button :disabled="pageNumber === 0" @click="prevPage"> Previous
                </button>
                <span v-if="pageNumber>0&&pageNumber < pageCount-1">
                    1... <b>{{pageNumber +1 }}</b> ... {{pageCount}}
                </span>
                <span v-if="pageNumber===0">
                    <b> 1 </b> ... <b style="word-space:2em">&nbsp;</b> ... {{pageCount}}
                </span>
                <span v-if="pageNumber===pageCount-1">
                    1  ... <b style="word-space:2em">&nbsp;</b> ... <b>{{pageCount}}</b>
                </span>
                <button :disabled="pageNumber >= pageCount -1 " @click="nextPage"> Next
                </button>
                <b style="word-space:2em">&nbsp;</b>
            </div>
        </div>
        <div id="right" class="column">
            <b-tabs>
                  <b-tab title="Info" active>
                        <ul class="groups">
                            <li
                                v-for="(content,group) in cur_balance" class="group_display"
                                v-if="group_index===content.Group_id">
                                <ul>
                                    <li v-for="(value,item) in content" v-if="item==='Group icon'">
                                        <b>{{item}}</b> : <img class='image' :src="value">
                                    </li>
                                    <li v-else>
                                        <b>{{item}}</b> : <i>{{value}}</i>
                                    </li>
                                </ul>
                            </li>
                        </ul>
                  </b-tab>

                  <b-tab title="User's in group" >
                        <div>
                            <ul class="group-display"
                            v-for="user in users_in_group"
                            v-if="user.group_id===group_index"
                            >
                                <li>
                                    {{ user.email }}
                                    <new_user_role
                                        v-if="user.user_role!='Owner'"
                                        v-bind:current_user_role="user.user_role"
                                        v-bind:user_email="user.email"
                                        v-bind:group_id="user.group_id"
                                        v-bind:getData="getData">
                                    </new_user_role>
                                </li>
                            </ul>
                            <add_user v-bind:group_id="selected_group_id" v-bind:getData="getData"></add_user>

                        </div>
                  </b-tab>
                  <b-tab title="Shared fund">
                      <div v-for="fund in shared_fund_list" v-if="group_index===fund.id_group"> {{ fund.name_fund }} </div>
                      <add_shared_fund v-bind:getData="getData" v-bind:group_id="selected_group_id"></add_shared_fund>
                  </b-tab>
                  <b-tab title="Shared spending categories">
                      <div v-for="spend in shared_spending_list" v-if="group_index===spend.id_group"> {{spend.name_cat }} </div>
                      <add_shared_spending v-bind:getData="getData" v-bind:group_id="selected_group_id"></add_shared_spending>
                  </b-tab>
            </b-tabs>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Add_new_user_to_group from '../components/Add_new_user_to_group';
    import Groups_registration from '../components/Groups_registration';
    import Add_shared_fund_to_group from '../components/Add_shared_fund_to_group';
    import Add_shared_category_to_group from '../components/Add_shared_category_to_group';
    import Change_users_role_in_group from '../components/Change_users_role_in_group';
    export default {
        name: "Groups",
        data() {
            return {
                cur_balance: [],
                users_group_list: [],
                selected_group_index: false,
                group_index: 0,
                pageNumber: 0,
                size:4,
                group_id: null,
                users_in_group: [],
                shared_fund_list: [],
                shared_spending_list: [],
                user_email: null,
                user_role: null
            }
        },
        components: {
            'add_user': Add_new_user_to_group,
            'create_new_group': Groups_registration,
            'add_shared_fund': Add_shared_fund_to_group,
            'add_shared_spending': Add_shared_category_to_group,
            'new_user_role': Change_users_role_in_group
        },
        methods: {
            selected_group: function (index, item) {
                this.selected_group_index = index;
                this.group_index = item;
                this.selected_group_id = item;
            },
            nextPage() {
                this.pageNumber++;
            },
            prevPage() {
                this.pageNumber--;
            },
            showModal() {
                this.$refs.myModalRef.show()
            },
            getData() {
                axios.get('api/v1/group/')
                    .then(response => {
                        this.cur_balance = response.data
                    })
                    .catch(e => {
                        this.errors.push(e)
                    }),
                    axios.get('api/v1/group/show_users_group_data')
                        .then(response => {
                            this.users_group_list = response.data
                        })
                        .catch(e => {
                            this.errors.push(e)
                        }),
                    axios.get('api/v1/group/show_users_in_group/')
                        .then(response => {
                            this.users_in_group = response.data
                        })
                        .catch(e => {
                            this.errors.push(e)
                        }),
                    axios.get('api/v1/fund/show_fund_by_group/')
                        .then(response => {
                            // JSON responses are automatically parsed.
                            this.shared_fund_list = response.data
                        })
                        .catch(e => {
                            this.errors.push(e)
                        }),
                    axios.get('api/v1/spending/show_spending_group/')
                        .then(response => {
                            // JSON responses are automatically parsed.
                            this.shared_spending_list = response.data
                        })
                        .catch(e => {
                            this.errors.push(e)
                        })
            }, deleteGroup: function (groupId) {
                let warning_alert;
                let warning=confirm("Delete group?");
                if (warning == true) {
                    warning_alert = "You delete group";
                    axios({
                        method: 'delete',
                        url: '/api/v1/group/delete_group/' + groupId,
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
            pageCount() {
                let l = this.users_group_list.length,
                    s = this.size,
                    pageMax = (l % s != 0) ? Math.floor(l / s) + 1 : Math.floor(l / s);
                return pageMax;
            },
            paginatedData() {
                const start = this.pageNumber * this.size,
                    end = (start + this.size <= this.users_group_list.length) ? start + this.size : this.users_group_list.length;
                return this.users_group_list
                    .slice(start, end);
            },
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
        font-size: large;
    }

    .image {
        height: 8vh;
        width: 8vh;
        background-color: lightskyblue;
        border-radius: 25%;
    }

    .groups {
        display: flex;
        flex-wrap: wrap;
    }
</style>
