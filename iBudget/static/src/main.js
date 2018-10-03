 import Vue from 'vue'
 import App from './App.vue'
 import Funds from './Funds'
 import Incomes from './Incomes'
 import Spendings from './Spendings'
 import Groups from './Groups'
 import 'v-calendar/lib/v-calendar.min.css'
 import VCalendar from 'v-calendar'
 import VueRouter from 'vue-router'
 import BootstrapVue from 'bootstrap-vue'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
Vue.use(BootstrapVue);
// Use v-calendar, v-popover components
Vue.use(VCalendar, {paneWidth:248});
Vue.use(VueRouter);

var routes = new VueRouter({
  routes: [

    { path: '/funds', component: Funds },
    { path: '/incomes', component: Incomes },
    { path: '/groups', component: Groups },
    { path: '/spendings', component: Spendings }

  ]
})
Vue.config.productionTip = false;
/* eslint-disable no-new */
new Vue({
  el: '#app',
  router: routes,
  render: h => h(App)
});




