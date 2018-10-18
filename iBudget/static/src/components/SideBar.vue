<template>
    <div id="side-bar">
        <aside>
            <div id="buttons">
                <b-button-group id="navbtns" vertical>
                    <b-button :variant="secondary" to="/login" v-show="!isLog">LOGIN</b-button>
                    <div v-show="isLog">
                        <b-button :variant="secondary" to="/home">HOME</b-button>
                        <b-button :variant="secondary" to="/funds">FUNDS</b-button>
                        <b-button :variant="secondary" to="/incomes">INCOMES</b-button>
                        <b-button :variant="secondary" to="/spendings">SPENDINGS</b-button>
                        <b-button :variant="secondary" to="/groups">GROUPS</b-button>
                        <b-button :variant="secondary" @click="logout">LOGOUT</b-button>
                    </div>
                </b-button-group>
            </div>
            <calendar></calendar>
        </aside>
    </div>
</template>

<script>

import axios from 'axios';
import Calendar from './Calendar';
import 'v-calendar/lib/v-calendar.min.css';

export default {
    name: "SideBar",

    components:{'calendar':Calendar},

    data(){
        return {
            isLog: document.cookie.search("sessionid=") !== -1
        }
    },

    created: function () {
        this.$router.history.current.path  === '/login' &&
        document.cookie.search("sessionid=") !== -1 &&
        this.$router.push({path:'home'})
    },

    methods:
    {
        logout: function (event) {
            axios({
                method: 'get',
                url: '/api/v1/authentication/logout/',
            }).then(response => {
                this.isLog = false;
                this.$router.push({path:'login'});
            });
        }
    }
}
</script>


<style scoped>
    aside {
        position: fixed;
        background: orange;
        float: left;
        width: 250px;
        height: 100vh;
    }

    #navbtns {
        width: 140px;
        margin-left: 55px;
        position: absolute;
        bottom: 275.2px;
        margin-bottom: 20px;
    }
</style>
