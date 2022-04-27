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
            <v-row>
                <v-card-text v-if="user_id == this.item.author">
                        <v-btn
                        class="ma-2"
                        outlined
                        color="indigo"
                        @click="updatePost()"
                        >
                        update post  
                        </v-btn>
                </v-card-text>
                <v-divider light></v-divider>
            </v-row>


            <Reply v-bind:reply_set="this.reply_set" v-bind:wrapper_id="this.wrapper_id" />
            
            
        </v-container>
    </v-app>
</template>

<script>
import axios from "axios";
import setToken from "../js_utils/token.js"
import parseDate from "../js_utils/date.js"
import Reply from "./Reply.vue"


export default {    
    data : () => {
        return {
            item:[],
            wrapper_id : -1,
            reply_set : [],
            user_id : -1
            }
        },

    methods : {
        parseDate,
        updatePost : function(){
            this.$router.push({
                name : "board_create",
                params : {
                    wrapper_id : this.wrapper_id,
                    category_id : 5,
                    update : true,  
                }
                })
        }
    },

    mounted() {
        let url = "http://127.0.0.1:8000/api/wrapper/"; 
        this.wrapper_id = this.$route.params.wrapper_id;
        let type = this.$route.params.content_type;
        this.user_id = localStorage.getItem('user');
        console.log(this.user_id);

        // type을 params로 끼워서 보내고
        // template도 type 별로 여러 개 만들고
        axios({
            method: "GET",
            url : url + this.wrapper_id ,
            headers : setToken(),
            params : {content_type : type}
        })
        .then(response => {
            
            this.item = response.data
            this.reply_set = response.data.reply_set
            console.log(this.item)
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