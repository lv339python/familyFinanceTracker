<template>
    <div id="icon_getter">
            <input type = image v-for="icon in icons" :src="icon.path"  v-on:click="get_name(icon.name)" class="icon" alt="icon"></input>
    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name:"Icon_getter",
        data () {
            return {
                    icons: [],
                    icon_name: "",
                   }
        },
        props: ['tabName'],

        created() {
            axios({
                method: "get",
                url: "api/v1/files/",
                params: {"tab": this.tabName}
            }).then(response => {
                this.icons = response.data;
            }).catch(error => {
                console.log(error.response.data);
            })
        },

        methods:{
            get_name: function(name){
            this.icon_name = name
            alert(this.icon_name)
            },
        }

    }
</script>

<style scoped>
    .icon {
        max-height: 64px;
        max-width: 64px;
        min-width: 32px;
        min-height: 32px;

    }
</style>
