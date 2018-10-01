import Vue from 'vue'
import App from './App.vue'
import axios from 'axios'
import VueAxios from 'vue-axios'
import Spending_history from './Spending_history'
import VueRouter from 'vue-router'
import Header from './Header.vue'
import Spend from './Spend'

var routes = new VueRouter({
  routes: [

    { path: '/app', component: App },
    { path: '/spending_history', component: Spending_history},
    { path: '/spending/set_limit', component: Spend},
  ]
})
Vue.use(VueRouter, axios)

new Vue({
  el: '#app',
  router: routes,
  render: h => h(Header)
});
