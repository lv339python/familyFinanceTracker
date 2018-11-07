<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            <img id="profile-thumbnail" rounded="circle"
                 blank width="16" height="16" alt="img" class="m-1"
                 src="http://cdn.onlinewebfonts.com/svg/img_191958.png"/>
            {{user.email}}
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Account">
            <div class="d-block text-center">
                <b-card>
                    <img id="profile-photo" rounded="circle" blank width="75" height="75"
                         blank-color="orange" alt="img" class="m-1"
                         src="http://cdn.onlinewebfonts.com/svg/img_191958.png"/>
                    <p class="card-text">
                        <b>Email: </b>{{user.email}}
                        <br/>
                        <b>First Name: </b>{{user.first_name}}
                        <br/>
                        <b>Last Name: </b>{{user.last_name}}
                    </p>
                    <b-btn class="mt-4" variant="outline-success" block @click="showInfo">Show more info</b-btn>

                        <div v-show="more_info">

                            <p class="card-text" v-for="item in custom">
                                <br/>
                                <b>Bio:</b>{{item.bio}}
                                <br/>
                                <b>Hobby:</b>{{item.hobby}}
                                <br/>
                                <b>Birthday:</b>{{item.birthday}}

                            </p>
                        </div>
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
            return {
                user: null,
                more_info:false,
                custom: []
            }
        },
        methods: {
            showInfo() {
                this.more_info=!this.more_info
            },
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
                    this.$router.push('/login');
                    this.$router.go();
                    this.hideModal();
                });
            }
        },
        created() {
            axios.get('api/v1/authentication/profile/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.user = response.data
                })
                .catch(e => {
                    this.errors.push(e)
                })
            axios.get('api/v1/custom_profile/show_custom_user_data')
                .then(response => {
                    this.custom = response.data
                })
        }
    }
</script>

<style scoped>
    #profile-photo {
        float: left;
    }

    .card-text {
        text-align: left;
        margin-left: 150px;
    }

    #acc {
        margin-right: 20px;
    }

    #profile-thumbnail {
        margin-right: 5px;
    }
</style>
