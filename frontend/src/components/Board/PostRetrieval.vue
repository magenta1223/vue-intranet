<template> 
    <v-container >
        <v-divider light></v-divider>
        <v-container class ="pa-4 ma-0">
            <v-divider light></v-divider>

            <v-row>
                <v-col>  
                    <v-card class="elevation-0">
                        <v-card-title class ="text-h2 active text-start"> 
                            {{this.item.title}}
                        </v-card-title>
                        <v-card-text class="text-start"> 
                            {{this.item.author}} &#183; {{parseDate(this.item.create_date, "YYYY-MM-DD HH:mm")}}
                        </v-card-text>
                        <v-divider light></v-divider>
                    </v-card>
                </v-col>
            </v-row>
            <v-row>
                <v-col>
                    <v-flex>
                        <v-card id = "content" class ="text-start elevation-0">
                            {{this.item.content}}
                        </v-card>
                    </v-flex>
                </v-col>
            </v-row>
            <v-row v-if="user_id == this.item.author" class="text-start">
                <v-col>
                    <v-btn
                    class="ma-2"
                    outlined
                    color="indigo"
                    @click="updatePost()"
                    justify="start"
                    >
                    update post  
                    </v-btn>

                    <v-btn
                    class="ma-2"
                    outlined
                    color="indigo"
                    @click="deletePost()"
                    justify="start"
                    >
                    delete post  
                    </v-btn>
                </v-col>
            </v-row>
            <v-divider light></v-divider>

            <Reply v-bind:reply_set="this.reply_set" v-bind:wrapper_id="this.wrapper_id" />
            
            
        </v-container>
    </v-container>
</template>

<script>
import axios from "axios";
import setToken from "../../js_utils/token.js"
import parseDate from "../../js_utils/date.js"
import Reply from "../BaseComponents/Reply.vue"

let url = "http://127.0.0.1:8000/api/wrapper/";

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
                name : "post_create",
                params : {
                    wrapper_id : this.wrapper_id,
                    category_id : this.category_id,
                    update : true,  
                }
                })
        },
        deletePost : function(){
            axios({
                method: "POST",
                url : url + 'delete/' + this.wrapper_id ,
                headers : setToken(),
                
                })
            .then(response => {
                this.$router.push({
                    name : "postlist",
                    params : {
                        
                        type : 'post',
                        category_id : this.category_id
                    }
                })
            })
            .catch(response => {
                console.log("Failed", response);
            });





        },

    },

    mounted() {
        let url = "http://127.0.0.1:8000/api/wrapper/"; 
        this.wrapper_id = this.$route.params.wrapper_id;
        this.category_id = this.$route.params.category_id;

        console.log(this.category_id);
        
        this.user_id = localStorage.getItem('user');
        console.log(this.user_id);

        // type을 params로 끼워서 보내고
        // template도 type 별로 여러 개 만들고
        axios({
            method: "GET",
            url : url + this.wrapper_id ,
            headers : setToken(),
            params : {content_type : 'post'}
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