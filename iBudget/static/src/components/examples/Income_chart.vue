<template>
    <div class="container">

         <div class="Chart">
          <h1 style="text-align:center;">Chart with incomes to funds:</h1>
          <line-example v-for="(dict, index) in amount_to_props"
                        v-bind:fund_name="Object.keys(dict)"
                        v-bind:x_axis="get_x"
                        v-bind:amounts="Object.values(dict)"
                        v-bind:color="getColor[index]"/>
        </div>


    </div>
</template>

<script>
    import LineExample from './LineExample';
    export default {
        components: {
            LineExample,
        },
        props: ['date_to_props', 'amount_to_props', 'income_to_props'],
        data() {


            return {
                height: 100,
            }
        },
        computed: {
            myStyles() {
                return {
                    height: `${this.height}px`,
                    position: 'relative'
                }
            },
            getColor() {
                var list = [];
                for (var ind in this.amount_to_props){
                    list.push("#" + Math.random().toString(16).slice(2, 8))
                }
                return list
                },
            get_x(){
                var x = [];
                for(var i=0; i<=this.date_to_props.length-1; i++){
                    x = x.concat(this.date_to_props[i][Object.keys(this.date_to_props[i])]);
                }
                return x
            }

            }


    }
</script>

<style>
    .container {
        max-width: 400px;
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
