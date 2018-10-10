<template>
<div id = "limit">
    <div id="available_spendings">
      <p>You can set limits for the following group spendings:
        <select v-model = "spending_category" required>
          <option v-for = "item in list_of_spendings">{{item}}</option>
        </select>
      </p>

    </div>

    <div id = "limit values">
      <form>
      <p>Start date:</p>
          <input v-model = "start_date" type = "text" placeholder = "yyyy-mm-dd" pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
          required size = "9">
          </input>
          <p>End date:</p>
          <input v-model = "end_date" type = "text" placeholder = "yyyy-mm-dd" pattern = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
          required size = "9">
          <p>Amount:</p>
          <input v-model = "value" type = "number" required>
          </input>
      </form>
    </div>
     <p><button v-on:click = 'set_limit'>set</button></p>
     <p>{{reply}}</p>
     <p><button v-show='isShown' v-on:click="reRender">OK</button></p>
</div>
</template>

<script>
    import axios from 'axios';
    export default {
     name: "Limit",
     data () {
        return {
        list_of_spendings: [],
        start_date: '',
        end_date: '',
        value: '',
        spending_category: '',
        reply: '',
        isShown: false
        }
     },
    created() {
      axios.get('api/v1/spending/admin/limit/')
    .then(response => {
      // JSON responses are automatically parsed.
      this.list_of_spendings = response.data;
    })
    .catch(e => {
      this.errors.push(e)
    })
     },
  methods: {
    set_limit: function (event) {
      axios({
              method: 'post',
              url: 'api/v1/spending/admin/set_limit/',
              data: {
                  'spending_category': this.spending_category,
                  'start_date': this.start_date,
                  'end_date': this.end_date,
                  'value': this.value,
                    },
             }).then(response =>{
                this.reply = response.data;
                this.isShown = true
             })
             .catch(function (error) {
                alert(error.response.data);
              });
    },
    reRender: function(event){
            if (this.isShown = true){
            this.$router.go('api/v1/spending/admin/set_limit/');
            }
     }

  }
}
</script>

<style scoped>

</style>
