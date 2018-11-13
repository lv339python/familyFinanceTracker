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
                    <div class="button">
                        <b-btn class="mt-3" variant="outline-success" @click="showInfo">Show more info</b-btn>
                        <b-btn class="mt-3" variant="outline-success" @click="addInfo">Update personal info</b-btn>
                    </div>
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
                            <input type="text" v-model="first_name"  class="form-control" placeholder="first name">
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="last_name" class="form-control" placeholder="last name">
                        </div>
                        <div class="form-group">
                            <textarea rows="10" cols="10" v-model="bio" class="form-control" placeholder="bio"></textarea>
                        </div>
                        <div class="form-group">
                            <input type="text" v-model="hobby" class="form-control" placeholder="hobby">
                        </div>
                        <div class="col-md-4">
                            <div class="form-group">
                                <input v-model="birthday" type="date" placeholder="birthday">
                            </div>
                        </div>


                        <div class="col-md-2">
                            <Upload_photo @get_name='onGet_name'></Upload_photo>
                         </div>

                        <!--<div class="col-md-4" v-model="icon">-->
                            <!--<button v-on:click="enable_upload" v-if="! upload">upload my own</button>-->
                            <!--<form enctype="multipart/form-data">-->
                                <!--<input type="file" name="icon" v-if="upload"-->
                                       <!--v-on:change="get_img_name_validate($event.target.files)"></input>-->
                            <!--</form>-->
                        <!--</div>-->

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
                        </div>
                    </div>
                </b-card>
            </div>
            <b-btn class="mt-3" variant="outline-danger" block @click="logout">Log Out</b-btn>
        </b-modal>
    </div>
</template>

<script>

    import axios from 'axios';
    import Upload_photo from './Upload_photo';


    export default {
        name: "Account",
        props: ["tabName"],
        components: {'Upload_photo': Upload_photo},

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
                icon: null,
                birthday: null,
                old_password: null,
                new_password: null,
                confirm_password: null,
                upload: false,
                maxFileSize: 60,
                password: null,
                selectedIcon: '',

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

            // enable_upload: function () {
            //     this.upload = true
            // },
            //
            // get_img_name_validate: function (file_list) {
            //     let img = file_list[0];
            //     let needed_type = /^\/*image/;
            //     this.icon = img;
            //     //here we validate the file type and size
            //     if (img.size > this.maxFileSize * 1024) {
            //         alert('The file you want to upload is too large. Please choose file smaller than 60 KB');
            //         return;
            //     }
            //     else if (!needed_type.test(img.type)) {
            //         alert('You chose incorrect file type, please choose image');
            //         return
            //     }
            //
            // },
            //
            // upload_emit_img: function (icon_name) {
            //     let formData = new FormData();
            //     formData.append('icon', this.image);
            //     axios({
            //         method: 'post',
            //         url: 'api/v1/files/',
            //         data: formData
            //     })
            //         .then(response => {
            //             this.reply = response.data;
            //             this.icon_name = this.reply.slice(55);
            //             this.$emit('get_name', {icon_name: this.icon_name});
            //         })
            //         .catch(function (error) {
            //             alert(error.response.data);
            //         })
            // },
            onGet_name(data) {
                this.selectedIcon = data['icon_name']
            },

            showInfo() {
                this.more_info = !this.more_info;
                if (this.add_info === true) {
                    return this.add_info = false
                }
            },
            addInfo() {
                this.add_info = !this.add_info;
                if (this.more_info === true) {
                    return this.more_info = false
                }
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
                    this.hideModal();
                    this.getData();
                    this.clearAll();
                })
            },

            addPersonalInfo: function (event) {
                console.log(
                    this.selectedIcon);
                axios({
                    method: 'post',
                    url: '/api/v1/custom_profile/create_personal_details/',
                    data: {
                        'first_name': this.first_name,
                        'last_name': this.last_name,
                        'bio': this.bio,
                        'hobby': this.hobby,
                        'icon': this.selectedIcon,
                        'birthday': this.birthday
                    }
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
        text-align: left;
        margin-left: 150px;
    }

    #acc {
        margin-right: 20px;
    }

    .button {
        margin: 10px;
    }

    #profile-thumbnail {
        margin-right: 5px;
    }
</style>
