<template>
    <div class="content">
        <div id="left" class="text column">
            <b-button :variant="secondary" to="/incomes/add">Add</b-button>
            <b-button :variant="secondary" to="/incomes/tracking">Tracking</b-button>
            <b-button :variant="secondary" to="/incomes/new">New</b-button>
        </div>
          <div  id="right" class="column">
            <div v-if="isList&& list.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'  v-if="list.length !== 0" @selected_item="delItem"/>
            </div>
            <router-view></router-view>
        </div>
    </div>

</template>

<script>
    import axios from 'axios';
    import List_paginated from '../components/List_paginated';
    export default {
        components: {'List_paginated': List_paginated},
        data() {
            return {
                isList: true,
                list: [],
                title: "Incomes",
                errors: [],
                id: 0
            }
        },
created() {
            axios({
                method: 'get',
                url: '/api/v1/income/'
            })
            .then(response => {
                this.list = response.data;
            })
            .catch(e => {
                this.errors.push(e)
            });
        },

        methods: {
            delItem(data) {
                if (data.id != 0) {
                    axios({
                        method: 'delete',
                        url: '/api/v1/income/delete_income/' + data.id,
                    }).then(response => {
                        this.$router.push('/incomes/')
                    })
                }
            }
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
</style>
