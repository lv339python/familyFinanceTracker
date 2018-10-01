<template>
    <div id="header">
      <aside>
        <router-view></router-view>
        <ul>
          <li>
            <router-link to="/spending/set_limit">Set spending limitation</router-link>
          </li>
          <li>
            <router-link to="/spending_history/">spend</router-link>
          </li>
        </ul>

      </aside>
</div>
</template>

<script>
    export default {
        name: "Header"
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
  #cal{
    width: inherit;
  }
</style>
