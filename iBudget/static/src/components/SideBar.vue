<template>
       <div id="header">
      <aside>
            <div id="buttons">
               <b-button-group id="navbtns" vertical>
                 <b-button :variant="secondary" to="/home">HOME</b-button>
                 <b-button :variant="secondary" to="/funds">FUNDS</b-button>
                 <b-button :variant="secondary" to="/incomes">INCOMES</b-button>
                 <b-button :variant="secondary" to="/spendings">SPENDINGS</b-button>
                 <b-button :variant="secondary" to="/groups">GROUPS</b-button>
            </b-button-group>
            </div>
      </aside>
    </div>
</template>

<script>
    export default {
        name: "SideBar"
    }
</script>

<style scoped>
aside{
  position:fixed;
  background: orange;
  float:left;
  width: 250px;
  height: 100vh;
}
#navbtns{
  width: 140px;
  margin-left: 55px;
  position: absolute;
  bottom: 275.2px;
  margin-bottom: 20px;
}
</style>
