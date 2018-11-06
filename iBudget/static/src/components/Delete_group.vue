<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Delete group
        </b-button>


        <b-modal ref="myModalRef" hide-footer title="Delete group">
            <div class="d-block text-center">
                <b-card>
                    <div>
                    <label>Chose group</label>
                    <select v-model="group_id" class="form-control">
                        <option v-for="group in group_list"
                                v-bind:value="group.id">
                            {{ group.name }}
                        </option>
                    </select>
                </div>

                    <b-btn class="button" variant="outline-primary" block @click="Delete">Delete group</b-btn>
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
                group_list: [],
                group_id: null
            }
        },

        created() {
            axios.get('/api/v1/group/get_by_group/')
                .then(response => {
                    // JSON responses are automatically parsed.
                    this.group_list = response.data;
                })
                .catch(e => {
                    this.errors.push(e)
                })
        },

        methods: {
            showModal() {
                this.$refs.myModalRef.show();

            },
            hideModal() {
                this.$refs.myModalRef.hide();

            },

            Delete: function (event) {
                axios({
                    method: 'put',
                    url: '/api/v1/group/delete_group/' + this.group_id,
                    data: {
                        'is_active': this.is_active
                    }
                }).then(response => {
                    this.$router.go('/groups/')
                })

            }
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
