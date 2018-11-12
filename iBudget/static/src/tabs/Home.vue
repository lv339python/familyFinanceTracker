<template>
    <div class="content">
        <div class="text">
            <div class="chartcontainer">
                <chart_spending
                    v-bind:value='value'
                    v-bind:name='name'  v-if="value.length !== 0" />
            </div>
        </div>
    </div>
</template>

<script>

    var x = new Date();
    var UTC = -x.getTimezoneOffset() / 60;

    import axios from 'axios';
    import Chart_spending from 'src/components/examples/Chart_spending';

    export default {
        name: "Home",
        components: {'Chart_spending': Chart_spending},
        data() {
            return {
                finish_date: x.toJSON().slice(0,10),
                start_date:  new Date(x.getFullYear(), x.getMonth(), 1, UTC+1).toJSON().slice(0,10),
                value: [],
                name: [],
                balance: [],
                initial:[],
                fund: []
            }
        },
        created() {
            axios({
                method: 'post',
                url: '/api/v1/spending_history/chart_spending/',
                data: {
                    'start_date': this.start_date,
                    'finish_date': this.finish_date,
                    'UTC': UTC
                }
            })
            .then(response => {
                this.name = response.data.name;
                this.value = response.data.value;
            })
            .catch(e => {
                this.errors.push(e)
            }),
            axios({
                method: 'get',
                url: '/api/v1/fund/get_balance/'
            })
            .then(response => {
                this.balance = response.data.balance;
                this.initial = response.data.initial;
                this.fund = response.data.fund;
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
        text-align: center;
    }

    p {
        width: 400px;
    }
</style>

