import Vue from 'vue'
import axios from 'axios'
import VueAxios from 'vue-axios'

Vue.use(VueAxios, axios)

 import Header from './Header'
 import Spend from './Spend'

 import VueRouter from 'vue-router'

Vue.use(VueRouter);
var routes = new VueRouter({
  routes: [
    { path: '/spending/set_limit', component: Spend},
]
})
Vue.config.productionTip = false;
/ eslint-disable no-new /
new Vue({
  el: '#app',
  router: routes,
  render: h => h(Header)
});
