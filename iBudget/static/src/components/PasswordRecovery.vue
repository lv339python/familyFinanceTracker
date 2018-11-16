<template>
    <div class="content">
        <div id="body">
            <div id="password_recovery">

                <h1>Change password</h1>
                <label>Please Enter New Password</label>
                <br/>
                <input required v-model="new_password" type="password" placeholder="New Password"/>
                <br/>
                <label>Please Confirm Your Password</label>
                <br/>
                <input required v-model="confirm_password" type="password" placeholder="Confirm Your Password"/>
                <br/>
                <div class="button">
                    <b-button class="btn btn-outline-primary" v-if=isValidPassword @click="setData">Submit</b-button>
                </div>
            </div>
        </div>
        <b-modal ref="myModalRef" hide-footer>
            <div class="d-block text-center">
                <p>Your password has been reset successfully!</p>
            </div>
            <div class="d-block text-right">
                <b-button variant="primary" @click="hideModal">OK</b-button>
            </div>
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

    .button {
        margin: 10px;
    }

    .content {
        height: 100vh;
        overflow: hidden;
        display: flex;
    }
</style>
