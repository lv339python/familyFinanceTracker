<template>
    <div class="Income_tracker">
    <div class="wrapper">
        <div id="total">
        <p>The total amount of income from the 1-st of this month till today is {{this.cur_income}}</p>
        </div>
        <div id="form">
            <p>Please choose dates below:</p>
            <p>Start date:</p>
            <input v-model = "start_date" type = "date" required>
            </input>
            <p>End date:</p>
            <input v-model = "end_date" type = "date" required>
            </input>
            <p><button v-on:click="sub_dates">submit</button></p>
        </div>

        <div id= "result">
            <table border='1px' v-if="shownResult">
                <caption>All the incomes for the chosen period:</caption>
                <tr><th>Income</th><th>Fund</th><th>Date</th><th>Amount</th><th>Comments</th></tr>
                <tr v-for="item in paginatedData">
                    <td>{{item['income']}}</td> <td>{{item['fund']}}</td> <td>{{item['date']}}</td> <td>{{item['amount']}}</td>
                    <td>{{item['comment']}}</td>
                </tr>
            </table>
            <div v-show="pageCount>1">
                    <button :disabled="paginated_page_number === 0" @click="prevPage"> Previous
                    </button>
                    <button :disabled="paginated_page_number>= pageCount -1 " @click="nextPage"> Next
                    </button>
            </div>
            <p><button v-on:click="reRender" v-if="shownResult">refresh</button></p>
        </div>

    </div>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name:"Income_tracker",
        data(){
            return{
                start_date: '',
                end_date: '',
                list_with_incomes: '',
                shownResult: false,
                cur_income: 0,
                // this is the size of a paginated page
                pagination_size: 3,
                paginated_page_number: 0,
            }
        },
        //props: ['tabName'],
        created(){
            axios.get('api/v1/income_history/get_cur_incomes/')
            .then(response => {
             this.cur_income = response.data;
            })
            .catch(e => {
                alert(error.response.data);
            });
        },

        computed:{
            pageCount(){
                let l = this.list_with_incomes.length,
                    s = this.pagination_size,
                    pageMax=(l % s != 0) ? Math.floor(l/s)+1 : Math.floor(l/s);
                return pageMax;
            },
            paginatedData(){
                const start = this.paginated_page_number * this.pagination_size,
                    end = (start + this.pagination_size <= this.list_with_incomes.length) ? start + this.pagination_size : this.list_with_incomes.length;
                return this.list_with_incomes
                .slice(start, end);
            }
        },


        methods: {
            sub_dates: function(){
                if(this.start_date.length!=0 && this.end_date.length!=0){
                    this.shownResult = true;
                    axios({
                        method: "post",
                        url: "api/v1/income_history/track/",
                        data: {
                            'start': this.start_date + "T00:00:00",
                            'end': this.end_date + "T23:59:59"
                        }
                    }).then(response => {
                        this.list_with_incomes = response.data;
                    }).catch(error => {
                        console.log(error.response.data);
                    })
                }else{
                    alert('You did not choose any dates or you chose only one date out of two required! Choose both dates!')
                };
            },
            reRender: function(){
                {this.$router.go('api/v1/income_history/track/');
                }
            },
            nextPage(){
                this.paginated_page_number++;
            },
            prevPage(){
                this.paginated_page_number--;
            }
        }
    }
</script>

<style>
    .wrapper{
        display:flex;
        flex-direction:column;
        margin: 0px auto;

    }
    caption{
        caption-side: top;
    }
    .Income_tracker{
        display:flex;
    }
</style>
