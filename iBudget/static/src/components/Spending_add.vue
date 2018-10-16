<template>
    <div id="spending_add">
        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label for="name">Name of spending:</label>
            <input v-model="newName" placeholder="Name" id="name">
           </div>
        </div>

        <div class="col-md-4">
            <hr>
            <div class="form-group">
                <label for="icon">Icon:</label>
                <select v-model="selectedIcon" class="form-control" id="icon">
                <option v-for="icon in icons" v-bind:value="icon.name"> {{ icon.show }} </option>
                </select>
             </div>
        </div>

        <div  v-show="isValidData">
           <hr>
           <button v-on:click="createSpending" :variant="secondary" >Create spending</button>
           <button v-on:click="createDone" :variant="secondary" v-show="isDone">{{msg}}</button>

        </div>
    </div>
</template>

<script>
import axios from 'axios';

    export default {
     name: "Spending_add",
     data () {
    return {
        icons:[{name: 'icon1.name',
                show: 'icon1.show'},
                {name: 'icon2.name',
                show: 'icon2.show'},
                ],
        isDone: false,
        newName: null,
        selectedIcon: null,
        newSpending: {
        'name': null,
        'icon': null
        },
        msg:''

    }
  },
  computed: {
      isValidData: {
          get: function(){
            var result =
                         this.selectedIcon !=null &&
                         this.newName!=null;
            return result;
          }
      }
},


  methods: {
    createSpending: function (event) {
      axios({
              method: 'post',
              url: '/api/v1/spending/add/',
              data: {
                  'name': this.newName,
                  'icon': this.selectedIcon
                }
             }).then(response =>(this.msg = response.data));
             this.isDone=true;
    },
    createDone: function (event) {
      this.$router.go('/spending_add')
    },
  }
}
</script>

<style scoped>

 </style>
