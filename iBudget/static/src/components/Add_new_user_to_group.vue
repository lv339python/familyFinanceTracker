<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Add user
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add new user to group">
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                        <b>{{group_id1}}</b>
                        <b>User's email</b>
                        <input type="email">
                        <br/>
                        <b>Admin </b>
                        <select>
                        <option>True</option>
                        <option>False</option>
                        <br/>
                    </p>
                    <b-button @click="addNewUser">Add</b-button>
                    <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Close Me</b-btn>
                </b-card>
            </div>
        </b-modal>
    </div>
</template>

<script>

    import axios from 'axios';

    export default {
        name: "new_user",
        props: ['group_id1'],
        methods: {
            showModal() {
                this.$refs.myModalRef.show()
            },
            addNewUser() {
                group_id: this.group_id1
            },
            hideModal() {
                console.log("hide");

                this.$refs.myModalRef.hide();
            }
        },
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
