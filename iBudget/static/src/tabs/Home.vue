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
                    @sliding-end="onSlideEnd" v-if="values.length !== 0">
            <b-carousel-slide img-blank v-for="(item, index) in dates" v-if="dates.length !== 0">
                <div class="text">
                    <div>
                        <div class="chartcontainer">
                            <chart_spending
                                v-bind:value='values[index].value'
                                v-bind:name='values[index].name'
                                v-bind:title='item'
                                v-if="values[index].value.length !== 0"/>
                        </div>
                        <b-btn v-b-toggle.collapse6 variant="primary">Balance</b-btn>

                        <b-collapse id="collapse6" class="mt-2">
                            <div class="table-holder">
                                <h4>Balance</h4>
                                <table class="table table-bordered">
                                    <thead>
                                    <tr>
                                        <th>Fund Name</th>
                                        <th>Initial Balance</th>
                                        <th>Current Balance</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    <tr v-for="(fundName, entry) in fund">
                                        <td>{{fundName}}</td>
                                        <td>{{initial[entry][index]}}</td>
                                        <td>{{balance[entry][index]}}</td>
                                    </tr>
                                    </tbody>
                                </table>
                            </div>
                        </b-collapse>
                    </div>
                </div>


            </b-carousel-slide>
        </b-carousel>
        <spending_button/>
        <income_button/>
        <financial_goal/>
        <fund_registration/>

    </div>
</template>

<script>

    var x = new Date();
    var UTC = -x.getTimezoneOffset() / 60;

    import axios from 'axios';
    import Chart_spending from 'src/components/examples/Chart_spending';
    import Spending_button from 'src/components/buttons/Spending_button';
    import Income_button from 'src/components/buttons/Income_button';
    import Financial_goal from 'src/components/Financial_goal';
    import Fund_registration from 'src/components/Funds_registration';
    import Delete_income from 'src/components/Delete_income';
    import Delete_fund from 'src/components/Delete_fund';
    import Delete_goal from 'src/components/Delete_goal';
    import Delete_spending from 'src/components/Delete_spending';

    export default {
        name: "Home",
        components: {
            'Chart_spending': Chart_spending,
            'Spending_button': Spending_button,
            'Income_button': Income_button,
            'Financial_goal': Financial_goal,
            'Fund_registration': Fund_registration,
            'Delete_income': Delete_income,
            'Delete_fund': Delete_fund,
            'Delete_goal': Delete_goal,
            'Delete_spending': Delete_spending,
        },
        data() {
            return {
                finish_date: x.toJSON().slice(0, 10),
                start_date: new Date(x.getFullYear(), x.getMonth(), 1, UTC + 1).toJSON().slice(0, 10),

                balance: [],
                initial: [],
                fund: [],
                dates: [],
                values: [],
                name: [],
                title: '',


            }
        },
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            }
        },
        created() {
            axios({
                method: 'get',
                url: '/api/v1/fund/get_balance/'
            })
                .then(response => {
                    this.balance = response.data.balance;
                    this.initial = response.data.initial;
                    this.fund = response.data.fund;
                    this.dates = response.data.dates;
                    this.values = response.data.values;
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
</style>

