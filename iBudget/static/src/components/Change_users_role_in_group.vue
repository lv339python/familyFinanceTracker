<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Change role
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add new user to group">
            <div class="d-block text-center">
                <b-card>
                    <p class="card-text">
                        <b>Do you want to change user's role?</b>
                    </p>
                    <b-btn class="mt-3" variant="outline-primary" block @click="saveData" aria-disabled="true">Yes</b-btn>
                    <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">No</b-btn>
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
            }
        },
        props: ["group_id", "getData"],
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
                this.clearAll();
            }
        },
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

    #profile-thumbnail {
        margin-right: 5px;
    }
</style>
