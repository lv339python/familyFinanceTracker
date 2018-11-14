import { Bar } from '../BaseCharts'

export default {
  extends: Bar,
   props: ['x_axis', "amounts", "color", "dates"],
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
          var datas = {
              labels:this.x_axis,
              datasets:[]
          };
          for (var dict in this.dates){
              var key = Object.keys(this.dates[dict]);
              var value = Object.values(this.dates[dict]);
              datas.datasets.push({label:key});
              datas.datasets[dict].fill = true;
              datas.datasets[dict].backgroundColor = this.color[dict];
              datas.datasets[dict].borderColor = this.color[dict];
              datas.datasets[dict].data = [];
              for (var val in value[0]){
                  datas.datasets[dict].data.push({x:value[0][val]});
              }
          }
          for (var dict in this.amounts){
              var value = Object.values(this.amounts[dict]);
              for (var val in value[0]){
                  datas.datasets[dict].data[val].y = value[0][val];
              }
          }
          this.datasets = datas
        },
    },
  mounted (){
    this.renderChart(this.datasets, {responsive: true, maintainAspectRatio: false})
  }
}
