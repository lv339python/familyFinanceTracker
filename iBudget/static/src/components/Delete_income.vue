<template>
     <div v-if="isList&& list.length!==0">
                <list_paginated
                    v-bind:list='list'
                    v-bind:title='title'
                    v-bind:deleteItem="deleteIncome"
                    v-if="list.length !== 0"/>
            </div>
</template>

<script>
    import axios from 'axios';
    import List_paginated from '../components/List_paginated';

    export default {
        name: "Delete_income",
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
        methods: {
            getData() {
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
            deleteIncome(incId) {
                if (incId) {
                    axios({
                        method: 'delete',
                        url: '/api/v1/income/delete_income/' + incId,
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
        created() {
            this.getData();
        }
    }
</script>

<style scoped>

</style>
