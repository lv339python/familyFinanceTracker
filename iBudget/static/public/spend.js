const months = [
    {nameM: 'All the year', valueM: 0},
    {nameM: 'January', valueM: 1},
    {nameM: 'February', valueM: 2},
    {nameM: 'March', valueM: 3},
    {nameM: 'April', valueM: 4},
    {nameM: 'May', valueM: 5},
    {nameM: 'June', valueM: 6},
    {nameM: 'July', valueM: 7},
    {nameM: 'August', valueM: 8},
    {nameM: 'September', valueM: 9},
    {nameM: 'October', valueM: 10},
    {nameM: 'November', valueM: 11},
    {nameM: 'December', valueM: 12}
    ]

new Vue({
  el: "#spending_set",
  data: {
    months: months,
    spending_list: [],
    aspend: null,
    selectedYear: null,
    selectedMonth: null,
    selectedIndex: 0,
    selectedValue: null,
    seen: true,
    newLimitation: {
    'year': null,
    'month': 0,
    'value': 0
    },
  },
  created: function() {
    this.getSpendingList();
  },
  computed: {
    spending_list: {
      // геттер:
      get: function () {
       console.log(this.spending_list)
        return this.spending_list;
      },
      // сеттер:
      set: function (newValue) {

        this.spending_list = newValue
        console.log(this.spending_list)
      }
    }
   },
  methods: {
    selectSpending: function(index) {
      this.aspend = this.spending_list[index]
      this.selectedIndex = index
    },

    setLimit: function() {
        console.log(this.selectedYear),
        console.log(this.selectedMonth),
        console.log(Number(this.selectedValue)),

        axios({
          method: 'post',
          url: "http://localhost:8000/spending/user/2/set_limit/"+String(this.aspend.id),
          data: {
            'year': Number(this.selectedYear),
            'month': Number(this.selectedMonth),
            'value':  Number(this.selectedValue),
          }
        });
//        location.reload();
        this.aspend: null,
     this.selectedYear: null,
     this.selectedMonth: null,
     this.selectedIndex: 0,
     this.selectedValue: null,
    },

    getSpendingList: function() {
    var v = this;
    axios.get('http://localhost:8000/spending/user/2/')
      .then(function (response ) {

          v.spending_list = response.data;
          console.log(v);

      }).catch(function (error) {
        console.log(error);
      })
    }
  }
});



