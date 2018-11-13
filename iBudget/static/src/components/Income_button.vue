<template>
    <div>
        <b-button class="btn btn-success btn-circle btn-xl" @click="showModal">
            +
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add new income">
            <div class="form-group">
               <input v-model="date" type="date">
            </div>

            <div class="calculator">
                <div class="display">
                     <div>
                        <b-input-group>
                            <b-form-input placeholder="0" v-model.number="current" type="number" min="1" ></b-form-input>
                            <b-select v-model="fund_category" v-b-popover.hover="'Choose fund'" title="Fund" variant="primary" slot="prepend"
                                       v-if="is_shared===false">
                           <option v-for="fund in fund_list" v-bind:value="fund.id"> {{ fund.name }}
                        </option>
                        </b-select>
                             <b-select  v-model="fund_category" v-b-popover.hover="'Choose Shared fund'" title=" Shared Fund" variant="primary" slot="prepend"
                                       v-if="is_active_group !== null && is_shared===true">
                            <option v-for="fund in shared_list"
                                v-if="fund.id_group === is_active_group"
                                v-bind:value="fund.id_fund">
                            {{fund.name_fund}}
                        </option>
                        </b-select>
                        </b-input-group>
                    </div>
                    <div class="col-md-12 form-group">
                        <input placeholder="✎ ✍ " v-model="comment" type="text" class="form-control">
                    </div>
                </div>

                <div @click="clear1" class="btn">C</div>
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
                <div>
                    <label>Select income category:</label>
                    <select v-model="inc_category">
                        <option v-for="income in income_list" v-bind:value="income.id"> {{ income.name }}
                        </option>
                    </select>
                      <div>
                    <input type="checkbox" id="cbx1" style="display:none" v-model="is_shared"/>
                    <label for="cbx1" class="toggle"><span></span>Shared</label>
                </div>
                     <b-btn v-b-toggle.collapse2 variant="primary">+</b-btn>
                </div>

                <div v-else>
                    <label>Chose group</label>
                    <select v-model="group">
                        <option v-for="group in group_list"
                                v-bind:value="group.id"
                                v-on:click="is_active_group=group.id">
                            {{ group.name }}
                        </option>
                    </select>
                </div>

                <div>
                    <b-button :disabled="DataValidation===false" class="btn btn-outline-primary"
                              @click="setData" :variant="success">Save
                    </b-button>
                </div>

                <div>
                    <b-button class="btn btn-outline-danger" @click="clear" :variant="warning">Clear form</b-button>
                </div>

            </b-collapse>

            <b-collapse id="collapse2" class="mt-2">
                <income_add/>
            </b-collapse>

        </b-modal>
    </div>

</template>

<script>
    import axios from 'axios';
    import Income_add from "src/components/Income_add";

    export default {
        name: 'Income_button',
        components: {
            'Income_add': Income_add,

        },
        data() {
            return {
                previous: null,
                current: 0,
                operator: null,
                operatorClicked: false,
                income_list: [],
                fund_list: [],
                group_list: [],
                shared_list: [],
                inc_category: null,
                fund_category: null,
                date: new Date().toJSON().slice(0, 10),
                comment: null,
                value:null,
                is_active_group: null,
                is_shared: false
            }
        },
        computed: {
            DataValidation: {
                get: function () {
                    let result =
                        this.inc_category != null &&
                        this.fund_category != null &&
                        this.current !== 0 &&
                        this.date != null;
                    return result;
                }
            }
        },
        created() {
            axios.get('/api/v1/income/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.income_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/fund/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('/api/v1/group/get_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.group_list = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('api/v1/income/show_income_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/income_history/register_income/',
                    data: {
                        'inc_category': this.inc_category,
                        'fund_category': this.fund_category,
                        'date': this.date,
                        'value': this.current,
                        'comment': this.comment,
                    }
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.$router.go('/Home/')
                }).catch(error => {
                    alert(error.response.data)
                })
            },
            clear() {
                this.group = null;
                this.inc_category = null;
                this.fund_category = null;
                this.date = null;
                this.comment = null;
                this.is_shared = null;
            },
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            },
            clear1() {
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
        max-height: 400px;
        min-width: 300px;
        max-width: 400px;
        min-height: 300px;
    }

    .display {
        grid-column: 1 / 5;
        background-color: #333;
        color: white;
    }

    .zero {
        grid-column: 1 / 3;
    }

    .btn-circle.btn-xl {
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
    .toggle {
        margin: 4vh;
        width: 40px;
        height: 20px;
        cursor: pointer;
        -webkit-tap-highlight-color: transparent;
        transform: translate3d(0, 0, 0);
    }

    .toggle:before {
        content: "";
        position: relative;
        top: 3px;
        left: 3px;
        width: 34px;
        height: 14px;
        display: block;
        background: #9A9999;
        border-radius: 8px;
        transition: background 0.2s ease;
    }

    .toggle span {
        position: absolute;
        top: 0;
        left: 0;
        width: 20px;
        height: 20px;
        display: block;
        background: white;
        border-radius: 10px;
        box-shadow: 0 3px 8px rgba(154, 153, 153, 0.5);
        transition: all 0.2s ease;
    }

    .toggle span:before {
        content: "";
        position: absolute;
        display: block;
        margin: -18px;
        width: 56px;
        height: 56px;
        background: rgba(79, 46, 220, 0.5);
        border-radius: 50%;
        transform: scale(0);
        opacity: 1;
        pointer-events: none;
    }

    #cbx1:checked + .toggle:before {
        background: #947ADA;
    }

    #cbx1:checked + .toggle span {
        background: #4F2EDC;
        transform: translateX(20px);
        transition: all 0.2s cubic-bezier(0.8, 0.4, 0.3, 1.25), background 0.15s ease;
        box-shadow: 0 3px 8px rgba(79, 46, 220, 0.2);
    }

    #cbx1:checked + .toggle span:before {
        transform: scale(1);
        opacity: 0;
        transition: all 0.4s ease;
    }

</style>
