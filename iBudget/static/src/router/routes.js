import Home from '../pages/Home'
import Funds from '../pages/Funds'
import Groups from '../pages/Groups'
import Spendings from '../pages/Spendings'
import Incomes from '../pages/Incomes'
export default [
  {
    path: '/incomes', component:Incomes
  },
  {
    path: '/home', component:Home
  },
  {
    path: '/funds', component:Funds
  },
  {
    path: '/groups', component:Groups
  },
  {
    path: '/spendings', component:Spendings
  }
];
