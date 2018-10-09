<template>
    <div id="spending_registration">
        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label >Select category:</label>
            <select v-model="category" class="ourform">
              <option v-for="spend in spending_list" v-bind:value="spend.id"> {{ spend.name }}
              </option>
            </select>
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose type_of_pay:</label>
            <select v-model="type_of_pay" class="ourform">
              <option v-for="type_of_pay in fund_list" v-bind:value="type_of_pay.id"> {{ type_of_pay.name }}
              </option>
            </select>
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input sum</label>
            <input v-model="sum" type="number" class="date">
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input comment</label>
            <input v-model="comment" type="text" class="date">
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose date</label>
            <input v-model="date" type="date">
           </div>
           <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose group</label>
            <select v-model="group" class="ourform">
            <option v-for="group in group_list"
                      v-bind:value="group.id"
                      v-on:click="is_active_shared_cat=group.id">
                      {{ group.name }}
            </option>
            </select>
          </div>
          <hr>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Chose category</label>
            <select v-model="shared_category" class="ourform" >
            <option v-for="shared_category in shared_list"
                      v-if="shared_category.id_group === is_active_shared_cat"
                      v-bind:value="shared_category.id">
                      {{ shared_category.name_cat }}
            </option>
            </select>
          </div>
          <hr>
        </div>


        <input type="checkbox" id="shared_button" v-model="is_shared">
        <label for="shared_button">Shared</label>
        <span>{{ is_shared }}</span>
        <button v-on:click="setData" :variant="secondary">Save</button>

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
            // shared_list2:[],
            category: null,
            type_of_pay: null,
            sum: null,
            date:null,
            comment:null,
            is_shared:false,
            group:null,
            is_active_shared_cat:null,
           }
        },
        created(){
          axios.get('/api/v1/spending/show_spending_ind/')
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
          axios.get('api/v1/spending/show_spending_group/')
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
                  'type_of_pay': this.type_of_pay,
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
