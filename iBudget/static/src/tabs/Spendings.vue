<template>
    <div class="content">
        <div class="text">
            <b-button :variant="secondary" to="../spending_registration">Spending Registration</b-button>
            <b-button :variant="secondary" to="../spend">Set individual limitation</b-button>
            <b-button :variant="secondary" to="/limit">Set group limitation</b-button>
            <b-button :variant="secondary" to="/add_spending">add spending</b-button>
            <Icon_getter :tabName="tab"></Icon_getter>

        </div>
    </div>
</template>

<script>
    import Icon_getter from '../components/Icon_getter.vue'
    export default {
        name: "Spendings",
        props: ["tabName"],
        data() {
        return {
            tab: 'spendings'
               }

        },
        components: {'Icon_getter': Icon_getter}

    }
</script>

<style scoped>
.content {
    height: 100vh;
    overflow: hidden;
    display: flex;
}
.text {
    width: fit-content;
    margin:  auto;
}
</style>
