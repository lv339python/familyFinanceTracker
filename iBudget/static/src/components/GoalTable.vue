<template>
    <div id ='goaltable'>
         <b-button :variant="secondary" to="/goal">Chart</b-button>
    <div class="ger" v-for="item in user_goal_list">
        <h3>{{item.value}} for '{{item.name}}' </h3>


       <table class="table table-bordered" >
                    <thead>
                        <tr>
                            <th>Contribution</th>
                             <th>Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(elem, index) in item.transaction" >
                            <td>{{elem}}</td>
                            <td>{{item.date_transaction[index]}}</td>

                        </tr>
                    </tbody>
                </table>
    </div>

    </div>
</template>

<script>
     import axios from 'axios';

    export default {
        name: "goaltable",
        data() {
            return {
                user_goal_list: [],
                start_date: null,
                finish_date: null,
                value: null,
                transaction: [],
                name: null,
                date_transaction: [],
                size: 3,
                pageNumber: 0,
            }
        },
        created() {
            axios.get('api/v1/fund/show_goal_data/')
                .then(response => {
                // JSON responses are automatically parsed.
                this.user_goal_list = response.data;
            this.transaction = this.user_goal_list[0].transaction;
            this.date_transaction = this.user_goal_list[0].date_transaction;
        })
        .
            catch(e => {
                this.errors.push(e)
        })
        },
          computed:{
        pageCount(){
            let l = this.transaction.length,
                s = this.size,
                pageMax=(l % s != 0) ? Math.floor(l/s)+1 : Math.floor(l/s);
            return pageMax;
        },
        paginatedData(){
            const start = this.pageNumber * this.size,
                end = (start + this.size <= this.transaction.length) ? start + this.size : this.transaction.length;
            return this.transaction
            .slice(start, end);
        }
    }
    }

</script>

<style scoped>

</style>
