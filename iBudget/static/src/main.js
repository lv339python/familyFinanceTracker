 import Vue from 'vue'
 import App from './App.vue'
 import 'v-calendar/lib/v-calendar.min.css';
 import VCalendar from 'v-calendar';

// Use v-calendar, v-popover components
Vue.use(VCalendar,);

Vue.config.productionTip = false;
/* eslint-disable no-new */
new Vue({
  el: '#app',
  render: h => h(App)
});




