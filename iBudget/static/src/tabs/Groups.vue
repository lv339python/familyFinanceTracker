<template>
    <div class="content">
        <div  id="left" class="text column">
            <b-button :variant="secondary" to="/groups/add" v-on:click="group_index=null">Create New Group</b-button>
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
            <ul class="groups">
                <li
                    v-for="(content,group) in cur_balance" class="group_display"
                    v-if="group_index===content.Group_id">
                    {{group}}
                    <ul>
                        <li v-for="(value,item) in content" v-if="item==='Group icon'">
                            {{item}} : <img class='image' :src="value">
                        </li>
                        <li v-else>
                            {{item}} : {{value}}
                        </li>
                        <add_user v-bind:group_id1="selected_group_id"></add_user>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';
    import Add_new_user_to_group from '../components/Add_new_user_to_group';
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
                group_id1: null,
                current_group_id: null
            }
        },
        components: {
            'add_user': Add_new_user_to_group
        },
        methods: {
            selected_group: function(index, item){
                this.selected_group_index = index
                this.group_index = item
                this.selected_group_id = item
            },
            nextPage(){
                this.pageNumber++;
            },
            prevPage(){
                this.pageNumber--;
            },
            showModal() {
                this.$refs.myModalRef.show()
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

            selected_group_id: {

                get: function () {
                     console.log("s_g_i get");
                  return this.current_group_id;
                },

                set: function (newValue) {
                 console.log("s_g_i set")
                  this.current_group_id = newValue;
                }
              }
        },
        created() {
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
                })
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
