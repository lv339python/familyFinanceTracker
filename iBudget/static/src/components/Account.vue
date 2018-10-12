<template>
    <div id="acc">
        <b-btn variant="primary" @click="showModal">
            Account
        </b-btn>
        <b-modal ref="myModalRef" hide-footer title="Account">
            <div class="d-block text-center">
                <b-card v-for="item in users_list">
                    <b-img id="profile-photo" rounded="circle" blank width="75" height="75"
                           blank-color="orange" alt="img" class="m-1"/>
                    <p class="card-text" >
                        <b>Email: </b>{{item.email}}
                        <br/>
                        <b>First Name: </b>{{item.first_name}}
                        <br/>
                        <b>Last Name: </b>{{item.last_name}}
                    </p>
                </b-card>
            </div>
            <b-btn class="mt-3" variant="outline-danger" block @click="logout">Log Out</b-btn>
        </b-modal>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Account",
        data() {
            return{
                users_list : []
            }
        },
        methods: {
            showModal() {
                this.$refs.myModalRef.show()
            },
            hideModal() {
                this.$refs.myModalRef.hide()
            },
            logout: function (event) {
            axios({
                method: 'get',
                url: '/api/v1/authentication/logout/',
            }).then(response => {
                this.isLog = false;
                this.hideModal();
            });
        }
        },
        created(){
            axios.get('api/v1/authentication/show_users_data')
                .then(response => {
            // JSON responses are automatically parsed.
            this.users_list = response.data
          })
          .catch(e => {
          this.errors.push(e)
          })
        }
    }
</script>

<style scoped>
    #profile-photo {
        float: left;
    }
    .card-text{
        text-align: left;
        margin-left: 150px;
    }
    #acc {
        margin-right: 20px;
    }
</style>
