import { Line } from '../BaseCharts'

export default {
  extends: Line,
   props: ['pieData', 'pieLabel'],
  mounted () {
    this.renderChart({
      labels:this.pieLabel,
      datasets: [
        {
          label: this.name,
          backgroundColor: '#f57979',
          data: this.pieData
        },

      ]
    }, {responsive: true, maintainAspectRatio: false})
  }
}
