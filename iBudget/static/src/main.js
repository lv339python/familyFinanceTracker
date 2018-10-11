import Vue from 'vue'
import App from './App.vue'
import router from './router/index'
import BootstrapVue from 'bootstrap-vue'
import axios from 'axios'
import VCalendar from 'v-calendar'


Vue.use(axios);
Vue.use(VCalendar, {paneWidth : 248});
Vue.use(BootstrapVue);



Vue.config.productionTip = false;
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: router,
  render: h => h(App)
});
