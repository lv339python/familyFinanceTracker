import Spending_history from '../tabs/Spending_history'
import {Home,Funds, Groups, Spendings, Incomes } from 'src/tabs';

import {Login} from "src/components"


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
  },
  {
    path: '/spending_history/', component:Spending_history
  },
  {
    path: '/login', component:Login
  }
];
