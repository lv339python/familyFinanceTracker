<template>
  <div id="app">

    <!--<date-picker v-model="time1" format="DD-MM-YYYY" lang="en" confirm></date-picker>-->
  <v-header></v-header>
    <div id="canvas">
      <keep-alive>
         <router-view></router-view>
      </keep-alive>
    </div>

  </div>

</template>


<script>

  import DatePicker from 'vue2-datepicker'
  import Header from './Header'

export default {
  components: { DatePicker, 'v-header':Header
  },
  data() {
    return {
      time1: '',
      time2: '',
      time3: '',
      shortcuts: [
        {
          text: 'Today',
          onClick: () => {
            this.time3 = [ new Date(), new Date() ]
          }
        }
      ],
      timePickerOptions:{
        start: '00:00',
        step: '00:30',
        end: '23:30'
      }
    }
  }
}

</script>
<style>

  #canvas{
    margin-left: 250px;
    background-color: whitesmoke;
  }
</style>
