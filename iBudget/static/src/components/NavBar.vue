<template>
    <div>
        <b-navbar id="nb" toggleable="md" type="dark" variant="info" sticky="true" v-if="checkLoginStatus()">

            <!-- Right aligned nav items -->

            <b-navbar-toggle class='burger-button' target="nav-collapse"></b-navbar-toggle>
            <!--<account></account>-->
            <!--<b-navbar-brand to="/login">Account</b-navbar-brand>-->
            <b-navbar-brand href="#" to="/home">iBudget</b-navbar-brand>
            <b-collapse is-nav id="nav-collapse">
                <b-navbar-nav>
                <b-nav-item href="#" to="/incomes">Incomes</b-nav-item>
                <b-nav-item href="#" to="/funds">Funds</b-nav-item>
                <b-nav-item href="#" to="/spendings">Spendings</b-nav-item>
                <b-nav-item href="#" to="/groups">Groups</b-nav-item>
            </b-navbar-nav>
            </b-collapse>

            <b-collapse>
                <!-- Right aligned nav items -->
                <b-navbar-nav>
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
    import 'v-calendar/lib/v-calendar.min.css'

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

    #nav_collapse {
        margin: auto;
    }

</style>
