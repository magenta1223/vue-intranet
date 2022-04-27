<template v-slot:default>
    <div class = "posting-container">
        <div class ="text-h2 active mb-2"> Category
        </div>
        <v-container >
            <v-layout> 
                <v-text-field v-model="title" placeholder="Title" name="title" type="text"></v-text-field>
            </v-layout>
            <!-- Text Editor : TipTap https://uxgjs.tistory.com/220 -->
            <v-layout> 
                <v-textarea
                v-model="content"
                name="input-7-4"
                value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
                ></v-textarea>
            </v-layout>
            <v-layout class="text-center btn-container">
                <v-btn
                        class="ma-2"
                        outlined
                        color="indigo"
                        @click="CUPost()"
                        >
                        Create!  
                        </v-btn>
            </v-layout>
        </v-container>
    </div>

</template>

<script>
import axios from "axios";
import setToken from "../js_utils/token.js"
import router from "../router/router.js"

let url = "http://127.0.0.1:8000/api/wrapper/";  // 장고 drf 서버 주소


export default {
    
    data : () => {
        return {
            title : "",
            content : "",
            update : false,
            category_id : -1,
            wrapper_id : -1

            }
        },

    components : {
    },
    
    // param이 바뀌어도 갱신이 되지 않음
    // board는 이미 mount가 끝났기 때문
    // 그래서 mounted를 call하지 않음
    // mounted를 method화 하고, param을 watch하면서 변경될때마다 call하면 됨
    methods: {
        CUPost : function(){
            console.log(this.category_id)

            if (this.update){
                console.log(url);
                this.category_id = 5
                console.log('update')
                axios({
                    method : "POST",
                    url : url + 'update/' + this.wrapper_id,
                    headers : setToken(),
                    params : {
                        content_type : "post",
                        category_id : this.category_id,
                        user_id : localStorage.getItem('user'),
                        title : this.title,
                        content: this.content
                    }
                })
                .then(
                    router.push({
                        name : "board",
                        params : {
                            category_id : this.category_id
                        }
                    })
                )
            } else {
                let category_id = this.$route.params.category_id
                axios({
                    method : "POST",
                    url : url,
                    headers : setToken(),
                    params : {
                        content_type : "post",
                        category_id : category_id,
                        user_id : localStorage.getItem('user'),
                        title : this.title,
                        content: this.content
                    }
                })
                .then(
                    router.push({
                        name : "board",
                        params : {
                            category_id : category_id
                        }
                    })
                )
            }


        },
    setValue : function(){

    }

    },

    mounted() {
        // update인 경우와 아닌 경우
        // update면 값을 미리 세팅해야 함
        this.update = this.$route.params.update
        let category_id = this.$route.params.category_id
        this.wrapper_id = this.$route.params.wrapper_id

        if (this.update) {
            let wrapper_id = this.$route.params.wrapper_id
            axios({
                method : "GET",
                url : url + wrapper_id,
                headers : setToken(),
                params : {
                    content_type : "post",
                }
            })
            .then(response => {
                console.log('get')
                this.wrapper_id 
            
                this.title = response.data.title
                this.content = response.data.content
            })
            .catch(response => {
                console.log("Failed", response);
            });
        }


    }

    }


</script>


<style scoped>
    .btn-container{
        margin-left: auto!important;
    }
</style>