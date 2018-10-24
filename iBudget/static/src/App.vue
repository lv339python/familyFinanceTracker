<template>
  <div class="flex-container" id="app">
    <!--<sidebar></sidebar>-->
      <navbar class="flex-element" id="navbar"></navbar>
      <router-view class="flex-element" id="view"></router-view>

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
    #navbar {

    }
    /*#canvas {*/
        /*background-color: whitesmoke;*/
        /*height: 100%;*/
    /*}*/
    .flex-container{
        height: 100vh;
        display: flex;
        flex-direction: column;
    }
    .flex-element{
        flex-grow: 1;
    }
    #view {
        background-color: whitesmoke;
        height: 100%;
    }
</style>
