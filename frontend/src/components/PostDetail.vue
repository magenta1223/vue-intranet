<template> 
    <v-app >
        <v-divider light></v-divider>
        <v-container class ="pa-4 ma-0">
            <v-divider light></v-divider>

            <v-row justify-center>
                <v-col> 
                    <v-flex> 
                        <v-card class ="elevation-0"> 
                            <v-flex id = "title" class ="text-h2 active">
                                    {{this.item.title}}
                            </v-flex>
                            <v-flex id = "author">
                                {{this.item.author}} &#183; {{parseDate(this.item.create_date, "YYYY-MM-DD HH:mm")}}
                            </v-flex>
                            <v-divider light></v-divider>
                        </v-card>
                    </v-flex>
                </v-col>
            </v-row>
            <v-row justify-center>
                <v-col>
                    <v-flex>
                        <v-card id = "content" class ="elevation-0">
                            {{this.item.content}}
                        </v-card>
                    </v-flex>
                </v-col>
            </v-row>
            <v-divider light></v-divider>

            <v-row>
                <v-col id = "reply">  
                    <v-textarea
                    v-model="reply"
                    name="input-7-4"
                    placeholder="댓글 작성란"
                    height=100
                    wrap row
                    ></v-textarea>
                </v-col>
            </v-row>

            <v-row>
                <v-col cols = "12">
                    <v-flex class = "btn-containter" xl-4>
                            <v-btn
                            class="ma-2"
                            outlined
                            color="indigo"
                            @click="create()"
                            >
                            Reply  
                            </v-btn>
                    </v-flex>
                </v-col>
            </v-row>
            <Reply v-bind:reply_set="this.reply_set" />
            <!--<v-row v-for="reply in reply_set" :key="reply.id">
                <v-col>
                    <v-sheet>
                        <v-card-text>
                            작성자 : {{reply.author}} 작성일자 : {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", true)}}
                        </v-card-text>
                        <v-card-text>
                            {{reply.content}} 
                        </v-card-text>
                        <v-divider></v-divider>

                    </v-sheet>
                </v-col>
            </v-row>-->

            
        </v-container>
    </v-app>
</template>

<script>
import axios from "axios";
import setToken from "../js_utils/token.js"
import parseDate from "../js_utils/date.js"
import Reply from "./Reply.vue"


let reply_url = "http://127.0.0.1:8000/api/reply/";

export default {    
    data : () => {
        return {
            item:[],
            reply : "",
            wrapper_id : -1,
            reply_set : [],
            user_id : -1
            }
        },

    methods : {
        parseDate,
        create : function(){
            axios({
                method : "POST",
                url : reply_url,
                headers : setToken(),
                params : {
                    // 어차피 board 전용임
                    "wrapper_id" : this.wrapper_id,
                    "reply" : this.reply,
                    "user_id" : localStorage.getItem('user')
                }
            })
            .then(response => { // arrow를 써야 this를 쓸 수 있다고 함
                this.reply = "";
                this.reply_set.push(response.data)
                }
            )
            
        },
    },

    mounted() {
        let url = "http://127.0.0.1:8000/api/wrapper/"; 
        this.wrapper_id = this.$route.params.wrapper_id;
        let type = this.$route.params.content_type;
        this.user_id = localStorage.getItem('user');
        console.log(this.user_id);

        // type을 params로 끼워서 보내고
        // template도 type 별로 여러 개 만들고
        url += this.wrapper_id;
        axios({
            method: "GET",
            url : url,
            headers : setToken(),
            params : {content_type : type}
        })
        .then(response => {
            this.item = response.data
            this.reply_set = response.data.reply_set
        })
        .catch(response => {
            console.log("Failed", response);
        });


    },

    components: {
        Reply
    }



    }


</script>

<style>

#title, #author, #time, #content, #reply {
    margin: 20px
}


.wrapper {
    width : 50%;
    margin-left: 100%;
    

}


</style>