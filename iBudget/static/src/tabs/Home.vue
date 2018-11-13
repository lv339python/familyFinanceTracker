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
                <b-carousel-slide img-blank  v-for="(item, index) in values"  v-if="values.length !== 0">
                    <div class="text">
                        <div>
                            <div class="chartcontainer">
                                <chart_spending
                                    v-bind:value='item.value'
                                    v-bind:name='item.name'
                                    v-bind:title='dates[index]'
                                    v-if="item.value.length !== 0" />
                            </div>
                                <!--<div v-for="entry in balance" v-if="balance.length !== 0"> {{entry.balance}}</div>-->
                            {{balanceData.balance[index]}}-{{balanceData.fund[index]}}-{{balanceData.initial[index]}} - {{balanceData.dates[index]}}
                        </div>
                    </div>
               </b-carousel-slide>
            </b-carousel>
          <spending_button/>
        <income_button/>


         </div>
</template>

<script>

    var x = new Date();
    var UTC = -x.getTimezoneOffset() / 60;

    import axios from 'axios';
    import Chart_spending from 'src/components/examples/Chart_spending';
    import Spending_button from 'src/components/Spending_button';
    import Income_button from 'src/components/Income_button';

    export default {
        name: "Home",
        components: {
            'Chart_spending': Chart_spending,
            'Spending_button': Spending_button,
            'Income_button': Income_button
        },
        data() {
            return {
                finish_date: x.toJSON().slice(0,10),
                start_date:  new Date(x.getFullYear(), x.getMonth(), 1, UTC+1).toJSON().slice(0,10),
                balanceData:{
                    balance: [],
                    initial:[],
                    fund: [],
                    dates: []
                },
                values: [],
                name: [],
                title: '',


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
            }),
            axios({
                method: 'get',
                url: '/api/v1/fund/get_balance/'
            })
            .then(response => {
                this.balanceData = response.data;
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

