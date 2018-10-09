<template xmlns="http://www.w3.org/1999/html">
<div class="container pt-5" id="spending_history">
  <div class="row mb-3">
    <div class="col-md-4">
      <h1>Spending history</h1>
    </div>
    <div class="row">
      <div class="col-md-12 pt-2">
        <div>
          <label >Select category:</label>

            <select v-model="category" class="ourform">
              <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
              </option>
            </select>
          <div>{{ category }}</div>
          <label>Your your card:</label>

            <select v-model="card" class="ourform">
              <option v-for="card in fund_list" v-bind:value="card.id"> {{ card.name }}
              </option>
            </select>
          <div>{{ card }}</div>
          <label>Input sum</label>
          <input v-model="sum" type="number" class="date">
          <div>{{ sum }}</div>

          <label>Comment</label>
          <input v-model="comment" type="text">
          <div>{{ comment }}</div>

          <label>Chose date</label>
          <input v-model="date" type="date">
          <div>{{ date }}</div>


          <label>Chose group</label>
          <select v-model="group" class="ourform">
              <option v-for="group in group_list"
                      v-bind:value="group.id"
                      v-on:click="is_active_shared_cat=group.id">
                      {{ group.name }}
              </option>
          </select>
            <label>Chose category</label>
            <select v-model="shared_category" class="ourform" >
              <option v-for="shared_category in shared_list"
                      v-if="shared_category.id_group === is_active_shared_cat"
                      v-bind:value="shared_category.id">
                      {{ shared_category.name_cat }}
              </option>
          </select>


          <input type="checkbox" id="shared_button" v-model="is_shared">
          <label for="shared_button">Shared</label>
          <span>{{ is_shared }}</span>

          <button v-on:click="setData">Save</button>
          <button>Cancel</button>

        </div>
        <hr>
      </div>

    </div>
  </div>
</div>
</template>


<script>
import axios from 'axios';
    export default {
        name: "spending_history",
        data() {
          return{
            spending_list: [],
            fund_list: [],
            group_list: [],
            shared_list: [],
            shared_category: null,
            shared_list2:[],
            category: null,
            card: null,
            sum: null,
            date:null,
            comment:null,
            is_shared:false,
            group:null,
            is_active_shared_cat:null,
           }
        },
        created(){
          axios.get('/api/v1/spending/show_spending')
            .then(response => {
            // JSON responses are automatically parsed.
            this.spending_list = response.data

          })
          .catch(e => {
          this.errors.push(e)
          });
          axios.get('api/v1/fund/')
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
          axios.get('api/v1/spending/show_spending_ind/')
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
              url: 'api/v1/spending_history/register_spending/',
              data: {
                  'category': this.category,
                  'card': this.card,
                  'date': this.date,
                  'sum': this.sum,
                  'comment': this.comment,
                  'is_shared':this.is_shared,
                  'group': this.group,

                }
             }).then(response =>{
                this.$router.go('/spending/set_limit')
             })
        },

          // getDisplayName(e){
          //   let value = e.target.value
          //   this.displayName = value
          //   },

          // shared: function (event) {
          //   this.is_shared = true
          // },
        }
}
</script>


<style>
  .date{
    width: 230px;
  }
  .ourform{
    width:250px;
  }
  .oursumanddate{
    width:233px;
  }
</style>
