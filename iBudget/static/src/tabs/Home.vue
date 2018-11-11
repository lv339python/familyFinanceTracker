<template>
    <div class="content">
        <b-carousel id="carousel1"
                        style="text-shadow: 1px 1px 2px #333;"
                        controls
                        indicators
                        img-width="1024"
                        img-height="500"
                        :interval="false"
                        v-model="slide"
                        @sliding-start="onSlideStart"
                        @sliding-end="onSlideEnd"v-if="values.length !== 0" >
                <b-carousel-slide img-blank  v-for="(item, index) in values" v-if="values.length !== 0">
        <div class="text">
                {{fund_balance}}
                <div>
                    <div class="chartcontainer">
                <chart_spending
                    v-bind:value='item.value'
                    v-bind:name='item.name'
                    v-bind:title='dates[index]'
                    v-if="item.value.length !== 0" />
            </div>
            </div>
        </div>
                   </b-carousel-slide>
            </b-carousel>
          <div>  {{data.fund_balance}}-{{data.fund_initial}}-{{fund_name}}</div>
          <calculator/>
        <income_button/>
         </div>
</template>

<script>

    var x = new Date();
    var UTC = -x.getTimezoneOffset() / 60;

    import axios from 'axios';
    import Chart_spending from 'src/components/examples/Chart_spending';
    import Calculator from 'src/components/Calculator';
    import Income_button from 'src/components/Income_button';

    export default {
        name: "Home",
        components: {'Chart_spending': Chart_spending,
                    'Calculator': Calculator,
                    'Income_button': Income_button},
        data() {
            return {
                finish_date: x.toJSON().slice(0,10),
                start_date:  new Date(x.getFullYear(), x.getMonth(), 1, UTC+1).toJSON().slice(0,10),
                values: [],
                name: [],
                title: '',
                fund_initial: null,
                fund_balance: null,
                fund_name:'',
                data: [],

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
                this.values = response.data.values;
                this.dates = response.data.dates;
            })
            .catch(e => {
                this.errors.push(e)
            });
            axios.get('/api/v1/fund/get_balance/')
                .then(response => {
                    this.fund_initial = response.data.fund_initial;
                    console.log(fund_initial);
                    this.fund_balance = response.data.fund_balance;
                    console.log(fund_balance);
                    this.fund_name = response.data.name;
                })
                .catch(e => {
                    this.errors.push(e)
                });
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
        margin: ;
        text-align: center;
    }

    p {
        width: 400px;
    }
</style>

