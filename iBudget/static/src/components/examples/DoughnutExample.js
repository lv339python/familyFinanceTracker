import { Doughnut } from '../BaseCharts'

export default {
  extends: Doughnut,
     props:['pieData', 'pieLabel'],
  mounted () {
    this.renderChart({
      labels:this.pieLabel,
      datasets: [
        {
          backgroundColor: [
                '#41B883',
                '#E46651',
                '#00D8FF',
                '#DD1B16',
                '#17a2b8',
                '#28a745',
                '#fd7e14',
          ],
          data: this.pieData
        }
      ]
    }, {responsive: true, maintainAspectRatio: false})
  }
}
