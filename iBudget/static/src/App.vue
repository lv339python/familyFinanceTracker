<template>
  <div id="app">
    <date-picker v-model="time1" format="DD-MM-YYYY" lang="en" confirm></date-picker>
    <calendar></calendar>
  </div>

</template>

<
<script>
  import DatePicker from 'vue2-datepicker'
  import Calendar from './Calendar'

export default {
  components: { DatePicker , 'calendar':Calendar
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
  #app{
  float: left;
  /*background-color: orange;*/
  /*padding-top: 60%;*/
}
</style>
