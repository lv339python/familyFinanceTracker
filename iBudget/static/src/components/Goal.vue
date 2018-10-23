<template>
    <div class="content" id="goal">
        <div class="text">

            <ul>
                <il v-for="goal in user_goal_list"> {{ goal.name}} - {{ goal.value
                    }}-{{goal.transaction}}-{{goal.date_transaction}}- {{goal.finish_date}}
                </il>
            </ul>
            <ul>
                <il v-for="goal in user_goal_list">
                    <chart1 v-bind:transaction="goal.transaction" v-bind:date_transaction="goal.date_transaction"
                            v-bind:value="goal.value"
                            v-bind:name="goal.name"></chart1>

                </il>
            </ul>

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
        .
            catch(e => {
                this.errors.push(e)
        })
        }
    }

</script>

<style scoped>
    .content {
        height: 100vh;
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }

    #goal {
        margin-right: 200px;
        width: 100%;
        height: 100vh;
        overflow: hidden;
        display: flex;
    }
</style>
