<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../Groups_registration">Create new group</b-button>
            <p>There are your groups: </p>
            <ul class="groups">
                <li v-for="(content,group) in cur_balance" class="group_display">
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
        font-size: large;
    }

    .image {
        height: 15vh;
        width: 15vh;
        background-color: aqua;
        border-radius: 5vh;
    }
</style>
