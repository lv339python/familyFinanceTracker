<template>
    <div class="content">
        <div id="body">
            <div id="password_recovery">

                <h1>Change password</h1>
                <label>Please enter new password</label>
                <br/>
                <input required v-model="new_password" type="password" placeholder="New password"/>
                <br/>
                <label>Please confirm your password</label>
                <br/>
                <input required v-model="confirm_password" type="password" placeholder="Confirm your password"/>
                <br/>
                <b-button class="btn btn-outline-primary" v-if=isValidPassword @click="setData">Submit</b-button>

            </div>
        </div>
        <b-modal ref="myModalRef" hide-footer>
            <div class="d-block text-center">
                <p>Your password has been reset successfully!</p>
            </div>
            <div class="d-block text-right">
            <b-button variant="primary"@click="hideModal">ok</b-button>

        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "PasswordRecovery",
        data() {
            return {
                new_password: null,
                confirm_password: null,
                token: this.$route.params["token"]
            }
        },
            computed: {
                isValidPassword: {
                    get: function () {
                        var result =
                            this.new_password === this.confirm_password;
                        return result;
                    }
                }
            },
            methods: {
                showModal() {
                this.$refs.myModalRef.show()
                },
                hideModal() {
                    this.$refs.myModalRef.hide()
                },
                setData: function (event) {
                    axios({
                        method: 'put',
                        url: '/api/v1/authentication/update_password/' + this.token,
                        data: {
                            'new_password': this.new_password,
                            'confirm_password': this.confirm_password

                        }

                    }).then(response => {
                    this.reply = response.data;
                    this.showModal()

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
