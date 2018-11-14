<template>
    <div>
        <b-button class="btn btn-danger btn-circle btn-xl" @click="showModal" data-toggle="tooltip"
                  title="Add spending">
            -
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add spending">
            <div class="form-group">
                <input v-model="date" type="date">
            </div>
            <div class="calculator">

                <div class="display">

                    <div>
                        <b-input-group>
                            <b-form-input id="curinput" v-model.number="current" type="number" min="1"></b-form-input>
                            <b-select v-model="type_of_pay" class="form-control" id="curinput" variant="primary" slot="prepend"
                                      v-show="groupId"
                                      v-b-popover.hover="'Choose Shared fund'" title=" Shared Fund"
                                      v-if="is_shared===true">
                                <option v-for="type_of_pay in shared_fund_list"
                                        v-if="type_of_pay.id_group===groupId"
                                        v-bind:value="type_of_pay.id_fund">
                                    {{ type_of_pay.name_fund }}
                                </option>
                            </b-select>
                            <b-select id="curinput" v-model="type_of_pay" class="form-control" variant="primary" slot="prepend"
                                      v-b-popover.hover="'Choose fund'" title="Fund"
                                      v-else>
                                <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id">
                                    {{ type_of_pay.name }}
                                </option>
                            </b-select>
                        </b-input-group>
                    </div>
                    <div class="col-md-12 form-group">
                        <input placeholder="✍" v-model="comment" type="text" class="form-control">
                    </div>
                </div>
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
                <b-btn v-b-toggle.collapse3 variant="primary">Choose Category</b-btn>
            </div>

            <b-collapse id="collapse3" class="mt-2"v-show="!visible">

                <div class="content">
                    <div class="row">
                        <div class="form-group " v-if="is_shared===true">
                            <p>Choose group:</p>
                            <div class="img_container">
                                <br>
                                <div v-for="group in group_list">
                                    <input type="image" :src="group.url" v-on:click="get_group_icon_id(group.id)"
                                           class="icon" alt="icon">
                                    <p>{{group.name}}</p>
                                </div>
                            </div>
                            <hr>
                            <div v-show="groupId">
                                <p>Select category:</p>
                                <div class="img_container">
                                    <br>
                                    <div v-for="category in shared_list" v-if="category.id_group === group_id">
                                        <input type="image" :src="category.url"
                                               v-on:click="get_group_icon_id(category.id_cat)"
                                               class="icon" alt="icon">
                                        <p>{{category.name_cat}}</p>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div class="form-group" v-else>
                            <p>Select category:</p>
                            <div class="img_container">
                                <br>
                                <div v-for="spend in spending_list">
                                    <input type="image" :src="spend.url" v-on:click="get_spend_icon_id(spend.id)"
                                           alt="icon" class="icon">
                                    <p>{{spend.name}}</p>
                                </div>
                            </div>
                            <b-btn v-b-toggle.collapse4 variant="primary">+</b-btn>
                        </div>

                        <div class="">
                            <input type="checkbox" id="cbx" style="display:none" v-model="is_shared"/>
                            <label for="cbx" class="toggle"><span></span>Shared</label>
                        </div>
                    </div>

                    <div>
                        <button type="button" class="btn btn-outline-danger" @click="reset">Reset</button>
                        <button :disabled="!isValidData" type="button" class="btn btn-outline-primary"
                                @click="setData"
                                :variant="secondary">Save
                        </button>
                    </div>
                </div>
            </b-collapse>
            <b-collapse id="collapse4" class="mt-2">

                <spending_add/>
            </b-collapse>
        </b-modal>
    </div>


</template>

<script>
    import axios from 'axios';
    import Spending_add from 'src/components/Spending_add';
    import Spending_registration from 'src/components/Spending_registration';

    export default {
        name: 'Spending_button',
        components: {
            'Spending_add': Spending_add,
            'Spending_registration': Spending_registration
        },
        data() {
            return {
                previous: null,
                current: 0,
                operator: null,
                operatorClicked: false,
                spending_list: [],
                fund_list: [],
                group_list: [],
                shared_list: [],
                shared_fund_list: [],
                groupId: null,
                category: null,
                type_of_pay: null,
                value: null,
                date: new Date().toJSON().slice(0, 10),
                comment: null,
                is_shared: false,
            }
        },
        computed: {
            isValidData: {
                get: function () {
                    var result =
                        this.category != null &&
                        this.type_of_pay != null &&
                        this.current !== 0 &&
                        this.date != null;
                    return result;
                }
            }
        },
        created() {
            axios.get('/api/v1/spending/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.spending_list = response.data.categories
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
            axios.get('api/v1/spending/show_spending_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                });
            axios.get('api/v1/fund/show_fund_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.shared_fund_list = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },
        methods: {
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/spending_history/register_spending/',
                    data: {
                        'category': this.category,
                        'type_of_pay': this.type_of_pay,
                        'date': this.date,
                        'value': this.current,
                        'comment': this.comment,
                        'group_id': this.groupId
                    }
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.$router.go('/spendings/add/')
                }).catch(error => {
                    alert(error.response.data)
                })
            },
            reset() {
                this.group = null;
                this.type_of_pay = null;
                this.current = null;
                this.date = null;
                this.comment = null;
                this.category = null;
                this.is_active_shared_cat = null;
                this.is_shared = false;
            },
            get_spend_icon_id(id) {
                this.category = id;
            },
            get_fund_icon_id(id) {
                this.type_of_pay = id
            },
            get_group_icon_id(id) {
                this.group_id = id;
                this.groupId = true;
            },
            get_group_fund_id(id) {
                this.type_of_pay = id
            },
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

    }

    .display {
        grid-column: 1 / 5;
        background-color: #333;
        color: white;
    }

    .zero {
        grid-column: 1 / 3;
    }

    .btn {
        border: 1px solid #999;
    }

    .operator {
        background-color: orange;
        color: white;
    }

    .btn-circle.btn-xl {
        width: 70px;
        height: 70px;
        padding: 10px 16px;
        border-radius: 35px;
        font-size: 24px;
        line-height: 1.33;
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

    #cbx:checked + .toggle:before {
        background: #947ADA;
    }

    #cbx:checked + .toggle span {
        background: #4F2EDC;
        transform: translateX(20px);
        transition: all 0.2s cubic-bezier(0.8, 0.4, 0.3, 1.25), background 0.15s ease;
        box-shadow: 0 3px 8px rgba(79, 46, 220, 0.2);
    }

    #cbx:checked + .toggle span:before {
        transform: scale(1);
        opacity: 0;
        transition: all 0.4s ease;
    }

    .img_container {
        width: 350px;
        max-height: 350px;
        overflow: scroll;
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
    }

    .icon {
        width: 70px;
        height: 70px;
    }

    div.img_container div {
        width: 70px;
        height: 95px;
    }
    #curinput{
       background-color: #333;
    }
</style>

