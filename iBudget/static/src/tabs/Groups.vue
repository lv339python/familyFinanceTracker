<template>
    <div class="content">
        <div  id="left" class="text column">
            <create_new_group v-bind:getData="getData"></create_new_group>
            <p>There are your groups: </p>
            <ul class="list-group">
            <li
                class="list-group-item list-group-item-action pointer"
                v-for="(item, index) in paginatedData"
                v-on:click="selected_group(index, item.id)"
                :class="{'active': selected_group_index===index}">
                <b> name </b>: <i> {{ item.group_name }} </i> <br>
                <b>your role </b>: <i> {{ item.user_role }} </i> <br>
                <b>count of users </b>: <i> {{ item.count }} </i>
            </li>
            </ul>
            <div v-show="pageCount>1">
                <button :disabled="pageNumber === 0" @click="prevPage"> Previous
                </button>
                <button :disabled="pageNumber >= pageCount -1 " @click="nextPage"> Next
                </button>
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
                            <ul class="list-group-item"
                            v-for="user in users_in_group" class="group_display"
                            v-if="user.group_id===group_index">
                                <li> {{ user.email }} - {{ user.user_role }} </li>
                            </ul>
                            <add_user v-bind:group_id="selected_group_id" v-bind:getData="getData"></add_user>
                            <delete_group v-bind:group_id="selected_group_id"></delete_group>
                        </div>
                  </b-tab>
                  <b-tab title="Shared fund and spending categories">
                        <add_shared_fund v-bind:group_id="selected_group_id"></add_shared_fund>
                        <add_shared_spending v-bind:group_id="selected_group_id"></add_shared_spending>
                  </b-tab>
            </b-tabs>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Add_new_user_to_group from '../components/Add_new_user_to_group';
    import Groups_registration from '../components/Groups_registration';
    import Delete_group from '../components/Delete_group';
    import Add_shared_fund_to_group from '../components/Add_shared_fund_to_group';
    import Add_shared_category_to_group from '../components/Add_shared_category_to_group';
    export default {
        name: "Groups",
        data() {
            return {
                cur_balance: [],
                users_group_list: [],
                selected_group_index: 0,
                group_index: 0,
                pageNumber: 0,
                size:5,
                group_id: null,
                users_in_group: []
            }
        },
        components: {
            'add_user': Add_new_user_to_group,
            'create_new_group': Groups_registration,
            'add_shared_fund': Add_shared_fund_to_group,
            'add_shared_spending': Add_shared_category_to_group,
            'delete_group':Delete_group
        },
        methods: {
            selected_group: function(index, item){
                this.selected_group_index = index;
                this.group_index = item;
                this.selected_group_id = item;
            },
            nextPage(){
                this.pageNumber++;
            },
            prevPage(){
                this.pageNumber--;
            },
            showModal() {
                this.$refs.myModalRef.show()
            },
            getData(){
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
                })
            }
        },
        computed:{
            pageCount(){
                let l = this.users_group_list.length,
                    s = this.size,
                    pageMax=(l % s != 0) ? Math.floor(l/s)+1 : Math.floor(l/s);
                return pageMax;
            },
            paginatedData(){
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
