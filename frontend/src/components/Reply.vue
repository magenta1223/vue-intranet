<template>
    <v-container>

        <v-row v-for="reply in reply_now" :key="reply.id">
            <v-col>
                
                <v-card class = "elevation0" outlined>
                    <div class = "box">
                        <v-card-text v-if="user_id == reply.author">
                            {{reply.author}} &#183; {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}} &#183; <a @click="update_reply(reply.id)">수정</a> &#183; <a @click="delete_reply(reply.id)">삭제</a>
                        </v-card-text>
                        <v-card-text v-else>
                            {{reply.author}} &#183; {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}}
                        </v-card-text>
                        <v-card-text>
                            {{reply.content}} 
                        </v-card-text>
                    </div>

                </v-card>
            </v-col>
        </v-row>
        <v-row justify="center">
            <v-col cols="8">
                <v-container class="max-width">
                    <v-pagination
                    v-model="page"
                    class="my-4"
                    :length="page_length"
                    ></v-pagination>
                </v-container>
            </v-col>
        </v-row>
    </v-container>
    

</template>


<script>
import parseDate from "../js_utils/date.js"

export default {
    data : () => {
        return {
            page: 1,
            page_length : 0,
            reply_now : [],
            }
        },
    

    props: ["reply_set"],

    methods : {
        parseDate,
        set_page : function(){
            this.page_length = parseInt(this.reply_set.length / 10) + 1 ;
        },
        paging : function(page){
            this.reply_now = this.reply_set.slice( (page-1) * 10, page * 10)
        },
        update_reply : function(d){
            console.log('여기?')
        }
    },

    watch : {
        'reply_set' : function(newParam, oldParam){
            this.set_page();
            this.paging(1);
        },
        'page' : function(newParam, oldParam){
            this.paging(newParam)
        }
    },

    mounted() {
        this.user_id = localStorage.getItem('user');
        console.log(this.user_id);
        
        this.set_page();
        

    }
}
</script>

<style scoped>

.box::before{
    content: "";
    position: absolute;
    top: 50%;     
    width: 15px;
    height: 15px;                    
    margin-top: -40px;               
    left:-8px;
    border-top: solid 0px;
    border-bottom: solid 1px;
    border-left: solid 1px;
    border-right: solid 0px;
    transform : rotate(45deg);
    border-color: rgba(0, 0, 0, 0.12);
    background-color: rgb(255, 255, 255);
    z-index: 1;
    box-shadow: 10px;
}

.elevation0{
    box-shadow: 1px;
}




</style>
