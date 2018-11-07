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

                    <b-btn class="mt-3" variant="outline-success" @click="showInfo">Show more info</b-btn>
                    <b-btn class="mt-3" variant="outline-success" @click="addInfo">Add info</b-btn>


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

                    <div v-show="add_info">
                        <div class="form-group">
                            <input type="text" v-model="first_name" class="form-control" placeholder="first name">
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="last_name" class="form-control" placeholder="last name">
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="bio" class="form-control" placeholder="bio">
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="hobby" class="form-control" placeholder="hobby">
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <input v-model="birthday" type="date" placeholder="birthday">
                            </div>
                        </div>
                        <b-btn class="mt-3" variant="outline-success" @click="addInfo">Save</b-btn>
                        <hr/>
                        <b-link @click="showForgotPassword">Deactivate your account</b-link>
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
                more_info: false,
                custom: [],
                add_info: false,
                first_name: null,
                last_name: null,
                bio: null,
                hobby: null,
                birthday: null

            }
        },
        methods: {
            showInfo() {
                this.more_info = !this.more_info;

            },
            addInfo() {
                this.add_info =!this.add_info;

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

            },
            setData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/custom_profile/create_personal_details/',
                    data: {
                        'first_name': this.first_name,
                        'last_name': this.last_name,
                        'bio': this.bio,
                        'hobby': this.hobby,
                        'photo': this.selectedIcon,
                        'birthday': this.birthday

                    },
                }).then(response => {
                    this.hideModal();
                    this.getData();
                    this.clearAll();
                })
            },
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
        text-align:left;
        margin-left: 150px;
    }

    #acc {
        margin-right: 20px;
    }

    #profile-thumbnail {
        margin-right: 5px;
    }
</style>
