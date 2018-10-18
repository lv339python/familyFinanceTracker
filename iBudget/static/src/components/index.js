import Login from './Login';
import Spend from './Spend';
import SideBar from './SideBar';
import Spending_registration from './Spending_registration';
import Limit from './Limit';
import Icon_getter from './Icon_getter';
import Goal from './Goal';


export {Login, SideBar, Spending_registration, Spend, Limit, Icon_getter, Goal, Chart};

import mixins from './mixins/index.js'

import {
  Pie,
  generateChart
} from './BaseCharts'

const VueCharts = {
  Pie,
  generateChart,
  render: () => console.error('[vue-chartjs]: This is not a vue component. It is the whole object containing all vue components. Please import the named export or access the components over the dot notation. For more info visit https://vue-chartjs.org/#/home?id=quick-start')
}

export default VueCharts

export {
  VueCharts,
  Pie,
  generateChart
}
