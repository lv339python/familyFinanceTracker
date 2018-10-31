<template>
    <div class="content">
        <div class="text">
        <h1> {{name}} {{value}} </h1>

        <h1> {{name_chart}} {{value_chart}} </h1>
            <div class="chartcontainer">


                    <chart_spending
                            v-bind:value="value_chart"
                            v-bind:name="name_chart"></chart_spending>


            </div>

        </div>
    </div>
</template>

<script>

    var x = new Date();
    var UTC = -x.getTimezoneOffset() / 60
    import axios from 'axios';
    import Chart_spending from 'src/components/examples/Chart_spending';

    export default {
        name: "Home",
    components: {'Chart_spending': Chart_spending},
        data() {
            return {
                start_date:  new Date(2018,9, 1).toJSON().slice(0,10),
                finish_date: new Date(2018, 9, 31).toJSON().slice(0,10),
                value: [],
                name: [],
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
                    })

        },
        computed: {
            value_chart: function () {
                return this.value
            },
            name_chart: function () {
                return this.name
            }
    }



    }


</script>
</script>

<style scoped>
    .content {
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
        text-align: center;
    }

    p {
        width: 400px;
    }
</style>

