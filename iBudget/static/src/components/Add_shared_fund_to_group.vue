<template>
    <div id="acc">
        <b-button variant="primary" @click="showModal">
            Add shared FundCategory
        </b-button>
        <b-modal ref="myModalRef" hide-footer title="Add shared FundCategory">
        <b-card>
            <label>Select fund:</label>
            <select v-model="shared_fund" class="form-control">
                <option v-for="fund in fund_list" v-bind:value="fund.id">
                    {{ fund.name }}
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
        name: "add_shared_fund",
        data() {
            return {
                shared_fund: null,
                fund_list: []
            }
        },
        props: ["group_id", "getData"],
        methods: {
            showModal() {
                this.$refs.myModalRef.show();
            },
            hideModal() {
                this.$refs.myModalRef.hide();
            },
            saveData: function (event) {
                axios({
                    method: 'post',
                    url: '/api/v1/group/add_shared_fund_to_group/',
                    data: {
                        'group_id': this.group_id,
                        'shared_fund': this.shared_fund
                    }
                }).then(response => {
                    this.hideModal();
                    this.getData();
                })
            },
        },
        created() {
            axios.get('/api/v1/fund/')
                .then(response => {
                    this.fund_list = response.data
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
