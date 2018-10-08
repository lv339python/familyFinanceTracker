<template>
  <div id="app">
    <sidebar></sidebar>
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
export default {
  components: { 'sidebar':SideBar
  }
}
</script>

<style>
  #canvas{
    margin-left: 250px;
    background-color: whitesmoke;
  }
</style>
