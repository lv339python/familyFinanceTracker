import { Line } from '../BaseCharts'

export default {
  extends: Line,
    props: ['x_axis', "amounts", "color"],
    data(){
      console.log('3',this.x_axis);
      return{
          datasets:{}
      }
    },
    created(){
        this.generateDatasets()
    },
    methods:{
      generateDatasets(){
          var datas = {
              labels:this.x_axis,
              datasets:[]
          };
          for (var dict in this.amounts){
              var key = Object.keys(this.amounts[dict]);
              var value = Object.values(this.amounts[dict]);
              datas.datasets.push({label:key});
              datas.datasets[dict].data = value[0];
              datas.datasets[dict].fill = false;
              datas.datasets[dict].borderColor = this.color[dict];


          }
          this.datasets = datas;
        }
    },

  mounted (){
    this.renderChart(this.datasets, {responsive: true, maintainAspectRatio: false})
  }
}
