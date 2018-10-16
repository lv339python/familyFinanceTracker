import {Home, Funds, Groups, Spendings, Incomes} from 'src/tabs';
import {Login, Spending_registration, Spend, Limit, Icon_getter} from "src/components";


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
    path: '/login', component:Login
  },
  {
    path: '/Spending_registration', component:Spending_registration
  },
  {
    path: '/spend', component:Spend
  },
  {
    path: '/limit', component: Limit
  },
  {
    path: '/add_spending', component: Icon_getter
  }
];
