<template v-slot:default>
    <v-container class = "posting-container">
        <v-row>
            <v-col class ="text-h2 text-start active mb-2"> Category
            </v-col>
        </v-row>
        <v-row>
            <v-col> 
                <v-text-field v-model="title" placeholder="Title" name="title" type="text"></v-text-field>
            </v-col>
            <!-- Text Editor : TipTap https://uxgjs.tistory.com/220 -->
        </v-row>
        <v-row>
            <v-col> 
                <v-textarea
                v-model="content"
                name="input-7-4"
                value="The Woodman set to work at once, and so sharp was his axe that the tree was soon chopped nearly through."
                ></v-textarea>
            </v-col>
        </v-row>
        <v-row class="text-start">
            <v-col class="btn-container">
                <v-btn
                        class="ma-2"
                        outlined
                        color="indigo"
                        @click="CUPost()"
                        >
                        Create!  
                        </v-btn>
            </v-col>
        </v-row>
    </v-container>

</template>

<script>
import axios from "axios";
import setToken from "../../js_utils/token.js"
import router from "../../router/router.js"

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
                        name : "post_retrieval",
                        params : {
                            category_id : this.category_id,
                            wrapper_id : this.wrapper_id,
                            content_type : 'post',
                        }
                    })
                )
            } else {
                let category_id = this.$route.params.category_id
                console.log(url)
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
                        name : "postlist",
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
        this.category_id = this.$route.params.category_id
        this.wrapper_id = this.$route.params.wrapper_id


        if (this.update) {
            axios({
                method : "GET",
                url : url + this.wrapper_id,
                headers : setToken(),
                params : {
                    content_type : "post",
                }
            })
            .then(response => {
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