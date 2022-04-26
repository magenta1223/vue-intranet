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
                        @click="create()"
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
            content : ""

            }
        },

    components : {
    },
    
    // param이 바뀌어도 갱신이 되지 않음
    // board는 이미 mount가 끝났기 때문
    // 그래서 mounted를 call하지 않음
    // mounted를 method화 하고, param을 watch하면서 변경될때마다 call하면 됨
    methods: {
        create : function(){
            console.log(this.category_id)
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

        },
    setValue : function(){

    }

    },

    mounted() {


    }

    }


</script>


<style scoped>
    .btn-container{
        margin-left: auto!important;
    }
</style>