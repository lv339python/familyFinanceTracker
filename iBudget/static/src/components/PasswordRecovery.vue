<template>
    <div class="content">
        <div id="body">
            <div id="password_recovery">

                <label>Change password</label>
                <br/>
                <input required v-model="new_password" type="password" placeholder="New password"/>
                <br/>
                <b-button @click="sendData">Submit</b-button>
                <label>token: {{token}}</label>
            </div>
        </div>
    </div>
</template>

<script>
    import axios from 'axios';


    export default {
        name: "PasswordRecovery",
        data() {
            return {
                new_password: null,
                token: this.$route.params["token"]
            }
        },
        methods: {

            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/authentication/update_password/',
                    data: {
                        'new_password': this.new_password
                    }
                }).then(response => {
                    this.$router.go('/Login/')
                })
            }
        }
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

