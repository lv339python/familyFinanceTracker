<template>
    <div> <b-button  class="btn btn-success btn-circle btn-xl" @click="showModal">
            +
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add new income">

    <div class="calculator">
        <div class="display">{{current || '0'}}</div>
        <div @click="clear" class="btn">C</div>
        <div @click="sign" class="btn">+/-</div>
        <div @click="percent" class="btn">%</div>
        <div @click="divide" class="btn operator">÷</div>
        <div @click="append('7')" class="btn">7</div>
        <div @click="append('8')" class="btn">8</div>
        <div @click="append('9')" class="btn">9</div>
        <div @click="times" class="btn operator">x</div>
        <div @click="append('4')" class="btn">4</div>
        <div @click="append('5')" class="btn">5</div>
        <div @click="append('6')" class="btn">6</div>
        <div @click="minus" class="btn operator">-</div>
        <div @click="append('1')" class="btn">1</div>
        <div @click="append('2')" class="btn">2</div>
        <div @click="append('3')" class="btn">3</div>
        <div @click="add" class="btn operator">+</div>
        <div @click="append('0')" class="btn zero">0</div>
        <div @click="dot" class="btn">.</div>
        <div @click="equal" class="btn operator">=</div>
        <b-btn v-b-toggle.collapse1 variant="primary">Choose Category</b-btn>
    </div>
             <b-collapse id="collapse1" class="mt-2">
                 <income_registration/>
            <income_add/>
                  </b-collapse>
          </b-modal>
            </div>
</template>

<script>
    import Income_add from "src/components/Income_add";
     import Income_registration from "src/components/Income_registration";
    export default {
        name: 'Income_button',
        components: {'Income_add': Income_add,
                     'Income_registration': Income_registration},
        data() {
            return {
                previous: null,
                current: '',
                operator: null,
                operatorClicked: false,
            }
        },
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            },
            clear() {
                this.current = '';
            },
            sign() {
                this.current = this.current.charAt(0) === '-' ?
                    this.current.slice(1) : `-${this.current}`;
            },
            percent() {
                this.current = `${parseFloat(this.current) / 100}`;
            },
            append(number) {
                if (this.operatorClicked) {
                    this.current = '';
                    this.operatorClicked = false;
                }
                this.current = `${this.current}${number}`;
            },
            dot() {
                if (this.current.indexOf('.') === -1) {
                    this.append('.');
                }
            },
            setPrevious() {
                this.previous = this.current;
                this.operatorClicked = true;
            },
            divide() {
                this.operator = (a, b) => a / b;
                this.setPrevious();
            },
            times() {
                this.operator = (a, b) => a * b;
                this.setPrevious();
            },
            minus() {
                this.operator = (a, b) => a - b;
                this.setPrevious();
            },
            add() {
                this.operator = (a, b) => a + b;
                this.setPrevious();
            },
            equal() {
                this.current = `${this.operator(
                    parseFloat(this.current),
                    parseFloat(this.previous)
                )}`;
                this.previous = null;
            }
        }
    }
</script>

<style scoped>
    .calculator {
        margin: 0 auto;
        width: 400px;
        font-size: 40px;
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        grid-auto-rows: minmax(50px, auto);
        max-height:400px;
        min-width:300px;
        max-width:400px;
        min-height:300px;
    }

    .display {
        grid-column: 1 / 5;
        background-color: #333;
        color: white;
    }

    .zero {
        grid-column: 1 / 3;
    }.btn-circle.btn-xl {
    width: 70px;
    height: 70px;
    padding: 10px 16px;
    border-radius: 35px;
    font-size: 24px;
    line-height: 1.33;
    }

    .btn {

        border: 1px solid #999;
    }

    .operator {
        background-color: orange;
        color: white;
    }

</style>
