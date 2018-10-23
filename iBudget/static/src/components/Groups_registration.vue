<template>
    <div id="Groups_registration">
        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label>Input name</label>
            <input type="text" v-model="name" class="form-control">
           </div>
          <div>{{ name }}</div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label >Choose icon</label>
            <select v-model="icon" class="form-control">
              <option >icon1</option>
              <option>icon2</option>
            </select>
           </div>
        </div>
        <button v-on:click="setData" :variant="secondary">Create</button>
    </div>
</template>

<script>
import axios from 'axios';
    export default {
        name: "Groups_registration",
        data() {
          return{
            name: null,
            icon: null
           }
        },
        methods: {

          setData: function (event) {
            axios({
              method: 'post',
              url: '/api/v1/group/create_new_group/',
              data: {
                  'name': this.name,
                  'icon': this.icon
                }
             }).then(response =>{
                this.$router.go('/group_registration/')
             })
          }
  }
}
</script>

<style scoped>
.content{
  height: 100vh;
  overflow: hidden;
  display: flex;
}
  .text{
    width: fit-content;
    margin:  auto;
  }
</style>
