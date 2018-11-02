import { Line } from '../BaseCharts'

export default {
  extends: Line,
    props: ['x_axis',"fund_name", "amounts", "color"],

  mounted (){
    this.renderChart(
        {
      labels: this.x_axis,
      datasets: [
        {
          label: this.fund_name,
          data:this.amounts[0],
            fill: false,
            borderColor: this.color

        }

      ]
    }
    , {responsive: true, maintainAspectRatio: false})
  }
}
