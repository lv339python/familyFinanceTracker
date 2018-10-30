<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="/groups/add">Create New Group</b-button>
            <p>There are your groups: </p>
            <ul class="groups">
                <li v-for="(content,group) in cur_balance" class="group_display">
                    {{group}}
                    <ul>
                        <li v-for="(value,item) in content" v-if="item==='Group icon'">
                            {{item}} : <img class='image' :src="value">
                        </li>
                        <li v-else>
                            {{item}} : {{value}}
                        </li>
                    </ul>
                </li>
            </ul>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Groups",
        data() {
            return {
                cur_balance: []
            }
        },
        created() {
            axios.get('api/v1/group/')
                .then(response => {
                    this.cur_balance = response.data
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
