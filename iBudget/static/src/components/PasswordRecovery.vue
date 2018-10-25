<template>
    <div class="content">
        <div id="body">
            <div id="password_recovery">

                <h1>Change password</h1>
                <label>Please enter new password</label>
                <br/>
                <input required v-model="new_password" type="password" placeholder="New password"/>
                <b-button class="btn btn-outline-primary" @click="setData">Submit</b-button>

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
                    method: 'put',
                    url: '/api/v1/authentication/update_password/'+ this.token,
                    data: {
                        'new_password': this.new_password,

                    }
                }).then(response => {
                    this.$router.push('/Login/')
                })
            }
        }
    }
</script>

<style scoped>

    #body {
        text-align: center;
        display: flex;
        margin: auto;
    }

    .content {
        height: 100vh;
        overflow: hidden;
        display: flex;
    }
</style>
