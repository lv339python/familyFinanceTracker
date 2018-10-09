import Home from '../tabs/Home'
import Funds from '../tabs/Funds'
import Groups from '../tabs/Groups'
import Spendings from '../tabs/Spendings'
import Incomes from '../tabs/Incomes'
import Spending_history from '../tabs/Spending_history'
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
  }

];
