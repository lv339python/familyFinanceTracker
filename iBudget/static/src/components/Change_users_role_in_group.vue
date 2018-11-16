<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            {{ current_user_role }}
        </b-button>
        <b-modal ref="myModalRef2" hide-footer :title=current_user_role>
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                        <b>Change User's Role?</b>
                        <br/>
                    </p>
                    <b-btn class="mt-3" variant="outline-primary" block aria-disabled="true" @click="saveData">Change Role</b-btn>
                    <b-btn class="mt-3" variant="outline-danger" block>Close</b-btn>
                </b-card>
            </div>
        </b-modal>
    </div>
</template>

<script>

    import axios from 'axios';

    export default {
        name: "new_user",
        data() {
            return {
                is_admin: false,
                email: null,
                new_user_role: null
            }
        },
        props: ["current_user_role", "user_email", "group_id", "getData"],
        methods: {
            changeRole: function(){
                if(this.current_user_role === 'Admin'){
                    this.new_user_role = 'Member'
                }
                else{
                    this.new_user_role = 'Admin'
                }
            },
            showModal() {
                this.$refs.myModalRef2.show();
                this.changeRole();
            },
            hideModal() {
                this.$refs.myModalRef2.hide();
            },
            saveData: function (event) {
                axios({
                    method: 'put',
                    url: '/api/v1/group/change_users_role_in_group/',
                    data: {
                        'group_id': this.group_id,
                        'user_email': this.user_email,
                        'is_admin': this.new_user_role
                    }
                }).then(response => {
                    this.hideModal();
                    this.getData();
                })
            }
        }
    }
</script>

<style scoped>
    .card-text {
        text-align: left;
        margin-left: 150px;
    }

    #acc {
        margin-right: 20px;
    }
</style>
