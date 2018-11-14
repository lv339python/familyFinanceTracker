<template>
    <div class="container">

        <div class="Chart">
            <h1 style="text-align:center;">Funds' income info:</h1>
            <line-example
                v-bind:x_axis="get_x"
                v-bind:amounts="amounts"
                v-bind:color="getColor"
                v-bind:dates="dates_from_props"/>
            <bar-example
                v-bind:x_axis="get_x"
                v-bind:amounts="amounts"
                v-bind:color="getColor"
                v-bind:dates="dates_from_props"/>
        </div>


    </div>
</template>

<script>
    import LineExample from './LineExample';
    import BarExample from './BarExample';

    export default {
        components: {
            LineExample,
            BarExample,
        },
        props: ['date_to_props', 'amount_to_props'],
        data() {
            return {
                height: 100,
                amounts: this.amount_to_props,
                x: null,
                dates_from_props: this.date_to_props
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
                for (var ind in this.amount_to_props) {
                    list.push("#" + Math.random().toString(16).slice(2, 8))
                }
                return list
            },
            get_x() {
                var x = [];
                for (var i = 0; i <= this.date_to_props.length - 1; i++) {
                    x = x.concat(this.date_to_props[i][Object.keys(this.date_to_props[i])]);
                }
                return x
            }
        },

    }
</script>

<style>
    .container {
        max-width: 800px;
        margin: auto;
    }

    h1 {
        font-family: 'Helvetica', Arial;
        color: #464646;
        text-transform: uppercase;
        border-bottom: 1px solid #f1f1f1;
        font-size: 28px;
        margin-top: 0;
    }

    .Chart {
        box-shadow: 0px 0px 20px 2px rgba(0, 0, 0, .4);
        border-radius: 20px;
    }

</style>
