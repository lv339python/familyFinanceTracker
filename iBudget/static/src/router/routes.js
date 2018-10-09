import {Spending_registration} from "src/components";
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
    path: '/Spending_registration', component:Spending_registration
  },
  {
    path: '/login', component:Login
  }
];
