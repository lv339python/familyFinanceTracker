<template>
    <div class="content">
        <div id="body">
            <div id="form">
                <form class="login" @submit.prevent="login" v-show="loginDisplay">
                    <h1>Login</h1>
                    <label>Email</label>
                    <br/>
                    <input required v-model="username" type="text" placeholder="Email"/>
                    <br/>
                    <label>Password</label>
                    <br/>
                    <input required v-model="password" type="password" placeholder="Password"/>
                    <hr/>
                    <b-button @click="login">Login</b-button>
                    <br/>
                    <br/>
                    <b-link @click="showForgotPassword">Forgot your password ?</b-link>
                    <br>
                    <b-link @click="showRegister">Create new account</b-link>
                    <hr/>
                    <b-button @click="google">Sign in With Google</b-button>
                </form>
                <form class="forgotpassword" @submit.prevent="forgotpassword" v-show="forgotpasswordDisplay">
                    <h1>Forgot password </h1>
                    <label>Please enter your email to change your password.</label>
                    <br/>
                    <input required v-model="email" type="text" placeholder="Email"/>
                    <b-button class="btn btn-outline-primary" @click="sendData">Send</b-button>
                </form>
                <form class="register" @submit.prevent="register" v-show="registerDisplay">
                    <h1>Register</h1>
                    <label>Email</label>
                    <br/>
                    <input required v-model="username" type="text" placeholder="Email"/>
                    <br/>
                    <label>Password</label>
                    <br/>
                    <input required v-model="password" type="password" placeholder="Password"/>
                    <br/>
                    <label>Password Confirmation</label>
                    <br/>
                    <input required v-model="confirm_password" type="password" placeholder="Confirm Password"/>
                    <hr/>
                    <b-button class="btn btn-outline-primary" type="submit" v-if:isValidPassword @click="registration">Register</b-button>
                    <br/>
                    <br/>
                    <b-link @click="showLogin">Already registered?</b-link>
                </form>
            </div>
        </div>
        <b-modal ref="myModalRef" hide-footer>
            <div class="d-block text-center">
                <p>We sent a letter  on your email. Please check your email to continue changing password !</p>
            </div>
            <div class="d-block text-right">
            <b-button variant="primary"@click="hideModal">ok</b-button>

        </b-modal>
    </div>

</template>

<script>
    import axios from 'axios';
    import router from 'src/router'

    export default {
        name: "Login",
        data() {
            return {
                loginDisplay: true,
                registerDisplay: false,
                forgotpasswordDisplay: false,
                password: null,
                confirm_password: null

            }
        },
        computed: {
            isValidPassword: {
                get: function () {
                    var result =
                        this.password === this.confirm_password;
                    return result;
                }
            }
        },
        methods: {

            navigate() {
                router.go(-1);
                //{router.push({name: 'Incomes'})
            },

            showRegister() {
                this.loginDisplay = false;
                this.registerDisplay = true;
                this.forgotpasswordDisplay = false;
            },

            showLogin() {
                this.loginDisplay = true;
                this.registerDisplay = false;
                this.forgotpasswordDisplay = false;


            },

            showForgotPassword() {
                this.loginDisplay = false;
                this.registerDisplay = false;
                this.forgotpasswordDisplay = true;
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
                }).then(response => {
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

                }).then(response => {
                    this.$router.push('/home');
                    this.$router.go('/home');
                }).catch(e => {
                    this.error = true;
                })
            },
            showModal() {
                this.$refs.myModalRef.show()
                },
                hideModal() {
                    this.$refs.myModalRef.hide()
                },
            sendData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/authentication/forgot_password/',
                    data: {
                        'email': this.email,

                    }
                }).then(response => {
                    this.reply = response.data;
                    this.showModal()
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
                })
            }
        },


    }
</script>
<style scoped>
    #body {
        text-align: center;
        display: flex;
        margin-top: 240px;
    }
    #form {
        margin: auto;
        width: fit-content;
        vertical-align: middle;
    }
</style>
