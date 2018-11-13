import { Line } from '../BaseCharts'

export default {
  extends: Line,
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
              datas.datasets[dict].fill = false;
              datas.datasets[dict].borderColor = this.color[dict];
              datas.datasets[dict].data = [];
              for (var val in value[0]){
                  //console.log("%%", value[0][val]);
                  datas.datasets[dict].data.push({x:value[0][val]});
              }
          }
          for (var dict in this.amounts){
              //var key = Object.keys(this.amounts[dict]);
              var value = Object.values(this.amounts[dict]);
              //datas.datasets.push({label:key});
              //datas.datasets[dict].fill = false;
              //datas.datasets[dict].borderColor = this.color[dict];
              //datas.datasets[dict].data = [];
              for (var val in value[0]){
                  console.log("%%", datas.datasets[dict].data[val]);
                  datas.datasets[dict].data[val].y = value[0][val];
              }
          }
          console.log('##',datas);
          this.datasets = datas
              // {labels:this.x_axis, datasets:[{
              // label:'asa',
              // data: [{x:"2018-10-01", y:5}, {x:"2018-10-05", y:10}, {x:"2018-10-20", y: 15}]},
              // {
              // label:'bdb',
              // data: [{x:"2018-10-01", y:5}, {x:"2018-10-04", y:23}]}
              // ]}
        }
    },
  mounted (){
    this.renderChart(this.datasets, {responsive: true, maintainAspectRatio: false})
  }
}
