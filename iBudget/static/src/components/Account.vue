<template>
    <div id="acc" class="mr-1">
        <b-button class='primary'  @click="showModal">
            <img id="profile-thumbnail" rounded="circle"
                 blank width="16" height="16" alt="img" class="m-1"
                 :src="getProfilePhoto()"/>
            {{user.email}}
        </b-button>
        <b-modal ref="myModalRef" size="lg" hide-footer title="Account">
            <div class="d-block text-center">
                <b-card>
                    <img id="profile-photo" rounded="circle" blank width="75" height="75"
                         blank-color="orange" class="m-1" :src="getProfilePhoto()"/>
                    <p class="card-text">
                        <b>Email: </b>{{user.email}}
                        <br/>
                        <b>First Name: </b>{{user.first_name}}
                        <br/>
                        <b>Last Name: </b>{{user.last_name}}
                    </p>
                    <div class="button">
                        <b-btn class="mt-3" variant="outline-success" @click="showInfo">Show more info</b-btn>
                        <b-btn class="mt-3" variant="outline-success" @click="addInfo">Update personal info</b-btn>
                        <b-btn class="mt-3" variant="outline-danger" @click="showDeleteModal">Deactivate profile</b-btn>
                    </div>
                    <div v-if="showMoreInfo">
                        <p class="card-text"></p>
                            <br/>
                            <b>Bio:</b>{{custom.bio}}
                            <br/>
                            <b>Hobby:</b>{{custom.hobby}}
                            <br/>
                            <b>Birthday:</b>{{custom.birthday}}
                        </p>
                    </div>

                    <div v-if="showAddInfo">
                        <div class="form-group">
                            <input type="text" v-model="user.first_name" class="form-control" placeholder="first name">
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="user.last_name" class="form-control" placeholder="last name">
                        </div>
                        <div class="form-group">
                            <textarea rows="10" cols="10" v-model="custom.bio" class="form-control"
                                      placeholder="bio"></textarea>
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="custom.hobby" class="form-control" placeholder="hobby">
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <input v-model="custom.birthday" type="date" placeholder="birthday">
                            </div>

                            <div class="col-md-2">
                                <Upload_photo @get_name='onGet_name'></Upload_photo>
                            </div>
                        </div>
                        <b-btn class="mt-3" variant="outline-success" @click="addPersonalInfo">Save</b-btn>
                        <hr/>
                        <div class="form-group">
                            <p>Update password</p>
                            <br/>
                            <input type="password" v-model="old_password" class="form-control"
                                   placeholder="current password">
                            <br/>
                            <input type="password" v-model="new_password" class="form-control"
                                   placeholder="new password">
                            <br/>
                            <input type="password" v-model="confirm_password" class="form-control"
                                   placeholder="confirm password">
                            <br/>
                            <b-btn class="mt-3" variant="outline-success" @click="setDatapassword">Save</b-btn>
                        </div>
                    </div>
                </b-card>
            </div>
            <b-btn class="mt-3" variant="outline-danger" block @click="logout">Log Out</b-btn>
        </b-modal>
        <b-modal ref="myModalDeleteRef" size="lg" hide-footer title="Delete your account">
            <div class="d-block text-center">
                <b-card>
                    <b-btn class="mt-3" variant="outline-danger" @click="Deactivate">Yes</b-btn>
                    <b-btn class="mt-3" variant="outline-danger" @click="hideDeleteModal">No</b-btn>
                </b-card>
            </div>
        </b-modal>
    </div>
</template>

<script>

    import axios from 'axios';
    import Upload_photo from './Upload_photo';

    const path = "https://s3.amazonaws.com/family-finance-tracker-static1/";
    const default_path = "http://cdn.onlinewebfonts.com/svg/img_191958.png";

    export default {
        name: "Account",
        props: ["tabName"],
        components: {'Upload_photo': Upload_photo},

        data() {
            return {
                user: null,
                showMoreInfo: false,
                custom: null,
                showAddInfo: false,
                old_password: null,
                new_password: null,
                confirm_password: null,
                upload: false,
                maxFileSize: 60
            }
        },

        computed: {
            isValidPassword: {
                get: function () {
                    return this.new_password === this.confirm_password && this.new_password !== "";
                }
            }
        },
        methods: {

            getProfilePhoto() {
                if (this.user.icon !== '') {
                    return path + this.user.icon;
                } else {
                    return default_path;
                }
            },


            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            },

            showInfo() {
                console.log(this.custom);
                this.showMoreInfo = !this.showMoreInfo;
                if (this.showAddInfo === true) {
                    return this.showAddInfo = false
                }
            },

            addInfo() {
                this.showAddInfo = !this.showAddInfo;
                if (this.showMoreInfo === true) {
                    return this.showMoreInfo = false
                }
            },

            showModal() {
                this.$refs.myModalRef.show()
            },

            hideModal() {
                this.$refs.myModalRef.hide()
            },
            showDeleteModal() {
                this.$refs.myModalDeleteRef.show()
            },

            hideDeleteModal() {
                this.$refs.myModalDeleteRef.hide()
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

            setDatapassword: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/authentication/change_password/',
                    data: {
                        'old_password': this.old_password,
                        'new_password': this.new_password,
                        'confirm_password': this.confirm_password
                    },
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.hideModal();
                    this.getData();
                    this.clearAll();
                })
            },

            addPersonalInfo: function (event) {
                console.log(
                    this.selectedIcon);
                console.log(this.user)
                console.log(this.custom)
                axios({
                    method: 'post',
                    url: '/api/v1/custom_profile/create_personal_details/',
                    data: {
                        'first_name': this.user.first_name,
                        'last_name': this.user.last_name,
                        'bio': this.custom.bio,
                        'hobby': this.custom.hobby,
                        'icon': this.selectedIcon,
                        'birthday': this.custom.birthday
                    }
                }).then(response => {
                    this.reply = response.data;
                    alert(this.reply);
                    this.hideModal();
                    this.getData();
                    this.clearAll();
                })
            },

            getData: function () {
                axios.get('api/v1/authentication/profile/')
                    .then(response => {
                        // JSON responses are automatically parsed.
                        this.user = response.data
                    })
                    .catch(e => {
                        this.errors.push(e)
                    });

                axios.get('api/v1/custom_profile/show_custom_user_data')
                    .then(response => {
                        this.custom = response.data;
                        console.log(this.custom);

                    });
            },

            Deactivate: function (event) {
                axios({
                    method: 'delete',
                    url: '/api/v1/authentication/delete_user/',

                }).then(response => {
                    this.$router.go('/login/')
                })
            }

        },


        created() {
            this.getData();
        }
    }
</script>

<style scoped>
    #profile-photo {
        float: left;
        border-radius: 50%;
    }

    .card-text {
        text-align: left;
        margin-left: 150px;
    }

    #acc {
        margin: auto;
        position: relative;

    }

    .button {
        margin: 10px;
    }

    #profile-thumbnail {
        margin-right: 5px;
        border-radius: 50%;
    }
</style>
