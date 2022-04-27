<template>
    <v-container>
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
                        @click="reply_create()"
                        >
                        Reply  
                        </v-btn>
                </v-flex>
            </v-col>
        </v-row>

        <v-row v-for="(reply, index) in repliesNowPage" :key="reply.id">
            <v-col>
                
                <v-card class = "elevation0" outlined>
                    <div class = "box">
                        <v-card-text v-if="user_id == reply.author">
                            {{reply.author}} &#183; {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}} &#183; <a @click="update_reply(reply, index)">수정</a> &#183; <a @click="delete_reply(reply, index)">삭제</a>
                        </v-card-text>
                        <v-card-text v-else>
                            {{reply.author}} &#183; {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}}
                        </v-card-text>

                        <v-container v-if="reply.update">
                            <v-row>
                                <v-col>  
                                    <!-- 이거 한 글자마다 수정됨 언젠가 봤던 그걸로 해결 -->
                                    <v-textarea 
                                    v-model="replyNow"
                                    name="input-7-4"
                                    height=100
                                    ></v-textarea>
                                </v-col>
                            </v-row> 
                            <v-row>
                                <v-btn
                                class="ma-2"
                                outlined
                                color="indigo"
                                @click="save_reply(reply, replyNow)"
                                >
                                Update  
                                </v-btn>
                            </v-row>                        
                        </v-container>
                        
                        <v-card-text v-else>
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
import axios from "axios";
import setToken from "../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/reply/";  // 장고 drf 서버 주소

export default {
    data : () => {
        return {
            page: 1, // 현재 댓글 페이지
            page_length : 0, // 댓글 페이지 길이
            reply : "", // 현재 작성중인 댓글
            repliesNowPage : [], // 현재 댓글 페이지에 표시할 댓글 목록
            updating_reply : -1, // 현재 수정중인 댓글
            replyNow : "", // 댓글 수정 내용

            }
        },
    

    props: ["reply_set", "wrapper_id"],

    methods : {
        parseDate,

        fetchReplies : function() {
            console.log('fetch', this.wrapper_id)

            axios({
                method: "GET",
                url : url + 'list/',
                headers : setToken(),
                params : {wrapper_id : this.wrapper_id}
            })
            .then(response => {
                this.reply_set = response.data.reply_set
                
            })
            .catch(response => {
                console.log("Failed", response);
            });

        },

        set_page : function(){
            this.page_length = parseInt(this.reply_set.length / 10) + 1 ;
        },

        paging : function(page){
            this.repliesNowPage = this.reply_set.slice( (page-1) * 10, page * 10)
        },

        reply_create : function(){
            axios({
                method : "POST",
                url : url,
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

        update_reply : function(reply, index){
            if (this.updating_reply > -1){
                this.repliesNowPage[this.updating_reply].update = false
            }
            this.updating_reply = index
            reply.update = true
            this.replyNow = reply.content
            this.paging(this.page); //새로고침 해야 textfield가 나옴
        },

        save_reply : function(reply, replyNow){
            reply.content = replyNow;
            axios({
                method: "POST",
                url : url + reply.id,
                headers : setToken(),
                params : {
                    // 어차피 board 전용임
                    "content" : replyNow
                }
            })
            .then((response) => {
                console.log('success')
            })
            .catch(response => {
                console.log("Failed", response);
            });
            reply.update = false
            this.updating_reply = -1

        },

        delete_reply : function(reply, index){
            axios({
                method: "POST",
                url : url + 'delete/' + reply.id,
                headers : setToken(),
            })
            .then((response) => {
                this.reply_set = response.data.reply_set
                console.log('success')
            })
            .catch(response => {
                console.log("Failed", response);
            });
            this.fetchReplies();
            
        
        }
    },

    computed: {
        item_length: function () {
            return this.reply_set.length;
        }
    },

    watch : {
        reply_set: {
            handler(newParam, oldParam){
                this.set_page();
                this.paging(this.page);
            },
            deep : true,
            immediate: true
        },
                
        'page' : function(newParam, oldParam){
            this.paging(newParam)
        }
    },

    mounted() {




        this.user_id = localStorage.getItem('user');
        for (let i in this.reply_set) {
            this.reply_set[i].update = false
        }

        this.set_page();
    },


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


.reply_update {
    margin : 15px;
}

</style>
