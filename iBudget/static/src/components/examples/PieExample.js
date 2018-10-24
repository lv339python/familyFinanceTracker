import { Pie } from '../BaseCharts'

export default {
  extends: Pie,
  props: ['pieData', 'pieLabel'],
  mounted () {
    this.renderChart({
      labels: this.pieLabel,
      datasets: [
        {
          backgroundColor: [
            '#41B883',
            '#E46651',
            '#00D8FF',
            '#DD1B16'
          ],
          data: this.pieData
        }
      ]
    }, {responsive: true, maintainAspectRatio: false})
  }
}
