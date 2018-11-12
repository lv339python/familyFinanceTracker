<template>
    <div class="container">

        <div class="Chart">
            <h1 style="text-align:center;">{{name}}</h1>
            <pie-example class="innerChart" v-bind:pieData="myPieData" v-bind:pieLabel="myPieLabel"/>
        </div>


    </div>
</template>

<script>
    import PieExample from './PieExample';

    export default {
        components: {
            PieExample,
        },
        props: ['transaction', 'date_transaction', 'value', 'name'],
        data() {
            let pieData = this.transaction;
            let Left = pieData.reduce((a, b) => a + b, 0);
            if (Left < 0) ;
            pieData.push(this.value - Left);

            let pieLabel = this.date_transaction;
            pieLabel.push('Left to goal');

            return {
                height: 100,
                myPieData: pieData,
                myPieLabel: pieLabel,
            }
        },
        computed: {
            myStyles() {
                return {
                    height: `${this.height}px`,
                    position: 'relative'
                }
            }
        }
    }
</script>

<style>
    .container {
        max-width: 600px;
        margin: auto;
    }

    h1 {
        font-family: 'Helvetica', Arial;
        color: #464646;
        text-transform: uppercase;
        border-bottom: 1px solid #f1f1f1;
        padding-bottom: 15px;
        font-size: 28px;
        margin-top: 0;
    }

    .Chart {
        padding: 20px;
        box-shadow: 0px 0px 20px 2px rgba(0, 0, 0, .4);
        border-radius: 20px;
        margin: 50px 0;
    }
    .innerChart {
        min-height: 300px;
        min-width: 200px;
    }
</style>
