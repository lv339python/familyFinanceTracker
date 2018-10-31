<template>
    <div class="container">

        <div class="Chart">
            <h1 style="text-align:center;">This month spending</h1>


            <h3 style="text-align:center;">2 {{value}} </h3>
            <h3 style="text-align:center;">3 {{this.value}} </h3>
            <h3 style="text-align:center;">4 {{this.name}} </h3>
            <h3 style="text-align:center;">35 {{myData}} </h3>

            <pie-example v-bind:pieData="myData" v-bind:pieLabel="myLabel"/>
        </div>



    </div>
</template>

<script>
    import PieExample from './PieExample';

    export default {
        components: {
            PieExample,
        },
        props: ['value', 'name'],
        data() {
            var myData = value;

            let myLabel = [];


            return {
                height: 100,
                myData: this.value,
                myLabel: this.name,
            }
        },
        computed: {
            myStyles() {
                return {
                    height: `${this.height}px`,
                    position: 'relative'
                }
            },
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
</style>
