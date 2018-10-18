<template>
    <div id="icon_getter">
            <input type = image
            v-for="icon in icons" :src="icon.path"
            v-on:click="get_name(icon.name)"
            class="icon" alt="icon"></input>

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

        created() {

            axios({
                method: "get",
                url: "api/v1/files/",
                headers: {
                'tab': 'funds'
                }
            }).then(response => {
                this.icons = response.data;
            }).catch(error => {
                console.log(error.response.data);
            })
        },

        methods:{
            get_name: function(name){this.$emit('get_name', {icon_name: name})},
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
