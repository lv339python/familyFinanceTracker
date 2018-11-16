<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Add Shared Spending Category
        </b-button>
        <b-modal ref="myModalRef1" hide-footer title="Add Shared Spending Category">
        <b-card>
            <label>Select Spending:</label>
            <select v-model="shared_spending" class="form-control">
                <option v-for="spend in spending_list" v-bind:value="spend.id">
                    {{ spend.name }}
                </option>
            </select>
            <b-btn class="mt-3" variant="outline-primary" block @click="saveData" aria-disabled="true">Save</b-btn>
            <b-btn class="mt-3" variant="outline-danger" block @click="hideModal">Close</b-btn>
        </b-card>
        </b-modal>
    </div>
</template>
<script>
    import axios from 'axios';
    export default {
        name: "add_shared_spending",
        data() {
            return {
                shared_spending: null,
                spending_list: []
            }
        },
        props: ["group_id", "getData"],
        methods: {
            showModal() {
                this.$refs.myModalRef1.show();
            },
            hideModal() {
                this.$refs.myModalRef1.hide();
            },
            saveData: function (event) {
                 axios({
                    method: 'post',
                    url: '/api/v1/group/add_shared_spending_to_group/',
                    data: {
                        'group_id': this.group_id,
                        'shared_spending': this.shared_spending
                    }
                }).then(response => {
                    this.getData();
                    this.hideModal();
                })
            },
        },
        created() {
            axios.get('/api/v1/spending/')
                .then(response => {
                    this.spending_list = response.data.categories
                })
                .catch(e => {
                    this.errors.push(e)
                })
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
