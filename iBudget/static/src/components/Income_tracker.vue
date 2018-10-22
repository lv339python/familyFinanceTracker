<template>
    <div id = "Income_tracker">
        <p>Start date:</p>
        <input v-model = "start_date" type = "date" placeholder = "yyyy-mm-dd" pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        required size = "9">
        </input>
        <p>End date:</p>
        <input v-model = "end_date" type = "date" placeholder = "yyyy-mm-dd" pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
        required size = "9">
        </input>
        <p><button v-on:click="sub_dates">submit</button></p>

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
                response: ''
            }
        },
        //props: ['tabName'],
        methods: {
            sub_dates: function(){
                axios({
                    method: "post",
                    url: "api/v1/income_history/track/",
                    //params: {"tab": this.tabName},
                    data: {
                        'start': this.start_date,
                        'end': this.end_date
                    }
                }).then(response => {
                    this.response = response.data;
                    alert(this.response)
                }).catch(error => {
                    console.log(error.response.data);
                })
            }
        }
    }

</script>
