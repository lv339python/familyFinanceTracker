<template>
    <div id="acc" class="mr-1">
        <b-button class='btn-yellow'  @click="showModal">
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
        margin: auto;
        position: relative;

    }

    #profile-thumbnail {
        margin-right: 5px;
    }

    .btn-yellow {
        color: #000000;
        background-color: #FFFFFF;
        border-color: #FFD105;
    }

    .btn-yellow:hover,
    .btn-yellow:focus,
    .btn-yellow:active,
    .btn-yellow.active,
    .open .dropdown-toggle.btn-yellow {
        color:#FFFFFF;
        background-color: #FFD105;
        border-color: #FFD105;
    }

    .btn-yellow:active,
    .btn-yellow.active,
    .open .dropdown-toggle.btn-yellow {
        background-image: none;
    }

    .btn-yellow.disabled,
    .btn-yellow[disabled],
    fieldset[disabled] .btn-yellow,
    .btn-yellow.disabled:hover,
    .btn-yellow[disabled]:hover,
    fieldset[disabled] .btn-yellow:hover,
    .btn-yellow.disabled:focus,
    .btn-yellow[disabled]:focus,
    fieldset[disabled] .btn-yellow:focus,
    .btn-yellow.disabled:active,
    .btn-yellow[disabled]:active,
    fieldset[disabled] .btn-yellow:active,
    .btn-yellow.disabled.active,
    .btn-yellow[disabled].active,
    fieldset[disabled] .btn-yellow.active {
        background-color: #FFFFFF;
        border-color: #FFD105;
    }

    .btn-yellow .badge {
        color: #FFFFFF;
        background-color: #000000;
    }
</style>
