<template>
    <div>
        <b-navbar toggleable="md" type="dark" variant="info" disabled>

            <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
            <account></account>
            <!--<b-navbar-brand to="/login">Account</b-navbar-brand>-->
            <b-navbar-brand to="/home" :disabled="isLog">Home</b-navbar-brand>
            <b-navbar-brand to="/incomes" :disabled="isLog">Incomes</b-navbar-brand>
            <b-navbar-brand to="/funds" :disabled="isLog">Funds</b-navbar-brand>
            <b-navbar-brand to="/spendings" :disabled="isLog">Spendings</b-navbar-brand>

            <b-collapse is-nav id="nav_collapse">

                <!-- Right aligned nav items -->
                <b-navbar-nav class="ml-auto">
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
        data() {
            return {
                isLog: document.cookie.search("sessionid=") !== -1
            }
        },
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
