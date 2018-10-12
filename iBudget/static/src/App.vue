<template>
  <div id="app">
    <!--<sidebar></sidebar>-->
      <navbar></navbar>

      <div id="canvas">
        <keep-alive>
           <router-view></router-view>
        </keep-alive>
      </div>
  </div>
</template>

<script>
import SideBar from './components/SideBar'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-vue/dist/bootstrap-vue.css'
import NavBar from './components/NavBar'
import Calendar from "./components/Calendar";

export default {
    components: {
        'sidebar' : SideBar,
        'navbar' : NavBar,
        'cal': Calendar
    }
}
</script>

<style>
    #canvas {
        background-color: whitesmoke;
    }
</style>
