<template>
    <div class='goaltable'>

            <b-carousel id="carousel1"
                        style="text-shadow: 1px 1px 2px #333;"
                        controls
                        indicators
                        img-width="1024"
                        img-height="500"
                        :interval="4000"
                        v-model="slide"
                        @sliding-start="onSlideStart"
                        @sliding-end="onSlideEnd" v-if="user_goal_list.length !== 0">
                <b-carousel-slide img-blank v-for="item in user_goal_list">
                    <div>
                        <div>
                            <chart1 v-bind:transaction="item.transaction"
                                    v-bind:date_transaction="item.date_transaction"
                                    v-bind:value="item.value"
                                    v-bind:name="item.name">
                            </chart1>
                        </div>

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
                </b-carousel-slide>
            </b-carousel>
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
                slide: 0,
                sliding: null
            }
        },
        created() {
            axios.get('api/v1/fund/show_goal_data/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.user_goal_list = response.data;
                    this.transaction = this.user_goal_list[0].transaction;
                    this.date_transaction = this.user_goal_list[0].date_transaction;
                    console.log(this.user_goal_list);
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            onSlideStart(slide) {
                this.sliding = true
            },
            onSlideEnd(slide) {
                this.sliding = false
            }
        }
    }

</script>

<style>
 .goaltable{
      width: fit-content;
        margin:0 ;
        text-align: center;
 }

</style>
