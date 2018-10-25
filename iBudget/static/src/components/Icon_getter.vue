<template>
    <div id="icon_getter">
        <p>Please choose the icon for your new {{tabName}} from the icons below or upload your own picture:</p>
        <input type=image
               v-for="icon in icons" :src="icon.path"
               v-on:click="get_name(icon.name)"
               class="icon" alt="icon" v-if="! upload"></input>
        <br>
        <br>
        <button class="btn btn-outline-success" v-on:click="enable_upload" v-if="! upload">upload my own</button>

        <form enctype="multipart/form-data">
            <input type="file" name="icon" v-if="upload"
                   v-on:change="get_img_name_validate($event.target.files)"></input>
        </form>
        <br>
        <button v-if="upload" v-on:click="upload_emit_img(icon_name)"> upload</button>
    </div>
</template>

<script>
    import axios from 'axios';

    export default {
        name: "Icon_getter",
        data() {
            return {
                icons: [],
                icon_name: "",
                upload: false,
                //size is in kB here
                maxFileSize: 60,
                reply: '',
                image: undefined
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

        methods: {
            get_name: function (name) {
                this.$emit('get_name', {icon_name: name})
            },

            enable_upload: function () {
                this.upload = true
            },

            get_img_name_validate: function (file_list) {
                let img = file_list[0];
                this.image = img;
                //here we validate the file type and size
                if (img.size > this.maxFileSize * 1024) {
                    alert('The file you want to upload is too large. Please choose file smaller than 100 KB');
                    return;
                }
                ;
                let needed_type = /^\/*image/;
                if (!needed_type.test(img.type)) {
                    alert('You chose incorrect file type, please choose image');
                    return;
                }
                ;
                this.icon_name = img.name;
            },

            upload_emit_img: function (icon_name) {
                this.$emit('get_name', {icon_name: this.icon_name});
                let formData = new FormData();
                formData.append('icon', this.image);
                axios({
                    method: 'post',
                    url: 'api/v1/files/',
                    data: formData,
                })
                    .then(response => {
                        this.reply = response.data;
                        alert(this.reply)
                    })
                    .catch(function (error) {
                        alert(error.response.data);
                    });
            }
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
