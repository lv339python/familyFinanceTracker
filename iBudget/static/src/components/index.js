import Login from './Login';
import Spend from './Spend';
import SideBar from './SideBar';
import Spending_registration from './Spending_registration';
import Limit from './Limit';
import Icon_getter from './Icon_getter';
import Goal from './Goal';
import mixins from './mixins/index.js';
import Spending_add from './Spending_add';
import Financial_goal from './Financial_goal';
import Spending_history from './Spending_history';
import Funds_registration from './Funds_registration';
import GoalTable from './GoalTable';

export {Login, SideBar, Spending_registration, Spend, Limit, Icon_getter, Spending_add,
    Financial_goal, Funds_registration, Spending_history, Goal, GoalTable};

import {Pie, generateChart} from './BaseCharts'

const VueCharts = {Pie, generateChart, render: () => console.error('[vue-chartjs]: This is not a vue component. It is the whole object containing all vue components. Please import the named export or access the components over the dot notation. For more info visit https://vue-chartjs.org/#/home?id=quick-start')
}


export default VueCharts

export {
  VueCharts,
  Pie,
  generateChart
}
