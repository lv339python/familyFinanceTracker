<template>
    <div>
        <b-navbar id="nb" toggleable="md" type="dark" variant="info" sticky="true" v-if="checkLoginStatus()">

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
            <!--<account></account>-->
            <!--<b-navbar-brand to="/login">Account</b-navbar-brand>-->
            <b-navbar-brand to="/home">Home</b-navbar-brand>
            <b-navbar-brand to="/incomes">Incomes</b-navbar-brand>
            <b-navbar-brand to="/funds">Funds</b-navbar-brand>
            <b-navbar-brand to="/groups">Groups</b-navbar-brand>
            <b-navbar-brand to="/spendings">Spendings</b-navbar-brand>
            <b-navbar-brand to="/groups">Groups</b-navbar-brand>
            <b-collapse is-nav id="nav_collapse">
                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
                    <account></account>
                    <calendar></calendar>
                </b-navbar-nav>
            </b-collapse>
        </b-navbar>
    </div>


</template>

<script>
    import Calendar from './Calendar'
    import Account from './Account'

    export default {
        name: "NavBar",

        components: {
            'calendar': Calendar,
            'account': Account
        },

        methods: {
            checkLoginStatus() {
                return (document.cookie.search("sessionid=") !== -1)
            }
        }
    }
</script>

<style scoped>
    #calendar {
        width: fit-content;
        height: fit-content;
    }

    /*#collapse1 {*/
    /*width: 250px;*/
    /*height: fit-content;*/
    /*}*/
</style>
