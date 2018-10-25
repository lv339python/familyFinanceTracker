<template>
    <div class='goaltable'>
        <div class="wrapper">
            <div class="row">
                <div class="ger" v-for="item in user_goal_list">
                    <div class="table-holder">
                        <h4>{{item.value}} for {{item.name}} should be achieved before {{item.finish_date}}</h4>
                        <table class="table table-bordered">
                            <thead>
                            <tr>
                                <th>Contribution</th>
                                <th>Date</th>
                            </tr>
                            </thead>
                            <tbody>
                            <tr v-for="(elem, index) in item.transaction">
                                <td>{{elem}}</td>
                                <td>{{item.date_transaction[index]}}</td>
                            </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>


            <div class="chartcontainer">

                <div v-for="goal in user_goal_list">
                    <chart1 v-bind:transaction="goal.transaction"
                            v-bind:date_transaction="goal.date_transaction"
                            v-bind:value="goal.value"
                            v-bind:name="goal.name"></chart1>
                </div>


            </div>
        </div>

    </div>
</template>

<script>
    import axios from 'axios';
    import Chart1 from 'src/components/examples/Chart1';

    export default {
        name: "Goal",
        components: {'Chart1': Chart1},
        data() {
            return {
                user_goal_list: [],
                start_date: null,
                finish_date: null,
                value: null,
                transaction: [],
                name: null,
                date_transaction: [],
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
                .catch(e => {
                    this.errors.push(e)
                })
        }
    }

</script>

<style scoped>
    .wrapper {
        display: flex;
        flex-direction: row;
        justify-content: space-around;
        align-items: end;
    }

    .chartcontainer {
        display: flex;
        justify-content: flex-end;

    }

    .row {
        flex-direction: column;

    }

</style>
