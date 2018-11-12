import { Line } from '../BaseCharts'

export default {
  extends: Line,
    props: ['x_axis', "amounts", "color"],
    data(){
      return{
          datasets:{}
      }
    },
    created(){
        this.generateDatasets()
    },
    methods:{
      generateDatasets(){
          // var datas = {
          //     //labels:this.x_axis,
          //     datasets:[]
          // };
          // for (var dict in this.amounts){
          //     var key = Object.keys(this.amounts[dict]);
          //     var value = Object.values(this.amounts[dict]);
          //     datas.datasets.push({label:key});
          //     datas.datasets[dict].data = value[0];
          //     datas.datasets[dict].fill = false;
          //     datas.datasets[dict].borderColor = this.color[dict];
          //
          //
          // }
          this.datasets = {labels:this.x_axis, datasets:[{
              label:'asa',
              data: [{x:"2018-10-01", y:5}, {x:"2018-10-05", y:10}, {x:"2018-10-20", y: 15}]}]}
        }
    },
// [ "2018-10-01", "2018-10-05", "2018-10-20" ] }, { "CARD2": [ "2018-10-01", "2018-10-04" ]
  mounted (){
    this.renderChart(this.datasets, {responsive: true, maintainAspectRatio: false})
  }
}
