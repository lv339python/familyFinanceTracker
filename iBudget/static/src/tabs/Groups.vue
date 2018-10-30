<template>
    <div class="content">
        <div class="text" class="coll-md-4">
            <b-button :variant="secondary" to="../Groups_registration">Create new group</b-button>
            <p>There are your groups: </p>
            <ul class="list-group">
            <li
                class="list-group-item list-group-item-action pointer"
                v-for="(item, index) in paginatedData"
                v-on:click="selected_group(index, item.id)"
                :class="{'active': selected_group_index===index}">
                {{ item.group_name }} - {{ item.user_role }}
            </li>
            <div v-show="pageCount>1">
                <button :disabled="pageNumber === 0" @click="prevPage"> Previous
                </button>
                <button :disabled="pageNumber >= pageCount -1 " @click="nextPage"> Next
                </button>
            </div>
        </div>

        <div class="text" class="coll-md-4">
            <ul class="groups">
                <li
                    v-for="(content,group) in cur_balance" class="group_display"
                    v-if="group_index===content.Group_id">
                    {{group}}
                    <ul>
                        <li v-for="(icon,item) in content" v-if="item==='Group icon'">
                            {{item}} : <img class='image' :src="icon">
                        </li>
                        <li v-else>
                            {{item}} : {{icon}}
                        </li>
                    </ul>
                </li>
            </ul>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Groups",
        data() {
            return {
                cur_balance: [],
                users_group_list: [],
                selected_group_index: 0,
                group_index: 0,
                pageNumber: 0,
                size:5
            }
        },
        methods: {
            selected_group: function(index, item){
                this.selected_group_index = index
                this.group_index = item
            },
            nextPage(){
                this.pageNumber++;
            },
            prevPage(){
                this.pageNumber--;
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
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
        font-size: large;
    }

    .image {
        height: 15vh;
        width: 15vh;
        background-color: aqua;
        border-radius: 5vh;
    }
</style>
