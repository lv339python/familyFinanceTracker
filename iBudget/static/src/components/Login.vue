<template>

  <div class="content">
      <div id="body">
            <p>Please login to continue</p>
           <div id="form">
              <form class="login" @submit.prevent="login" v-show="loginDisplay">
                <h1>Login</h1>
                <label>User name</label>
                <br/>
                <input required v-model="username" type="text" placeholder="Username"/>
                <br/>
                <label>Password</label>
                <br/>
                <input required v-model="password" type="password" placeholder="Password"/>
                <hr/>
                <b-button @click="login">Login</b-button>
                <br/>
                <br/>
                <b-link @click="showRegister">Create a new account</b-link>
                <hr/>
                <b-button @click="google">Sign in With Google</b-button>
              </form>

             <form class="register" @submit.prevent="register" v-show="registerDisplay" >
                <h1>Register</h1>
                <label>User name</label>
                <br/>
                <input required v-model="username" type="text" placeholder="Username"/>
                <br/>
                <label>Password</label>
                <br/>
                <input required v-model="password" type="password" placeholder="Password"/>
                <br/>
                <label>Password Confirmation</label>
                <br/>
                <input required v-model="password" type="password" placeholder="Password"/>
                <hr/>
                <b-button type="submit" @click="registration">Register</b-button>
               <br/>
               <br/>
               <b-link @click="showLogin">Already registered?</b-link>
             </form>
           </div>
      </div>
  </div>

</template>

<script>
import axios from 'axios';
import router from 'src/router'

export default {
    name: "Login",
    data() {
        return {
            loginDisplay:true,
            registerDisplay:false
        }
    },
    methods: {

        navigate() {
            router.go(-1);
            //{router.push({name: 'Incomes'})
        },

        showRegister(){
            this.loginDisplay = false;
            this.registerDisplay = true
        },

        showLogin(){
            this.loginDisplay = true;
            this.registerDisplay = false;
        },

        close() {
            this.$emit('close');
        },

        registration: function (event) {
            axios({
                method: 'post',
                url: '/api/v1/authentication/registration/',
                data: {
                    'email': this.username,
                    'password': this.password
                }
            }).then(response =>{
                this.loginDisplay = true;
                this.registerDisplay = false;
            }).catch(e => {
                this.error = true;
            })
        },

        login: function (event) {
            axios({
                method: 'post',
                url: '/api/v1/authentication/login/',
                data: {
                    'email': this.username,
                    'password': this.password
                }
            }).then(response =>{
                this.$router.go('/home');
            }).catch(e => {
                this.error = true;
                })
        },
        google: function (event) {
            axios({
                method: 'get',
                url: '/api/v1/authentication/auth/',
            }).then(response => {
                window.location.replace(response.data["url"]);
            }).catch(e => {
                this.error = true;
            });
        }
    },
}
</script>

<style scoped>
    .content {
        height: 100vh;
        overflow: hidden;
        display: flex;
    }

    .text {
        width: fit-content;
        margin: auto;
    }
</style>
