<template>
    <div id="fund_registration">

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
            <Icon_getter></Icon_getter>
           </div>
        </div>

        <div class="col-md-4">
          <hr>
          <div class="form-group">
            <label >Shared to</label>
            <select v-model="is_shared" class="form-control">
              <option > true
              </option>
              <option>false</option>
            </select>
           </div>
        </div>

        <button v-on:click="setData" :variant="secondary">Save</button>
    </div>
</template>

<script>
import axios from 'axios';
import Icon_getter from './Icon_getter.vue'
    export default {
        name: "fund_registration",
        data() {
          return{
            name: null,
            is_shared: false,
            icon: null
           }
        },
        components:{
            'Icon_getter': Icon_getter
        },
        methods: {

          setData: function (event) {
            axios({
              method: 'post',
              url: '/api/v1/fund/create_new_fund/',
              data: {
                  'name': this.name,
                  'is_shared': this.is_shared,
                  'icon': this.icon
                }
             }).then(response =>{
                this.$router.go('/create_new_fund/')
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
