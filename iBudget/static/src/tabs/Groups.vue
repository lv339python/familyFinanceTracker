<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../Groups_registration">Create new group</b-button>
            <ul id="groups">
                <li v-for="(content,group) in cur_balance" >
                  {{group}}
                    <ul>
                        <li v-for="(item,value) in content" >
                            {{value}} : {{item}}
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
        data () {
            return {
                cur_balance : []
            }
        } ,
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
        overflow: hidden;
        display: flex;
    }
    .text {
        width: fit-content;
        margin:  auto;
        font-size: x-large;
    }
</style>
