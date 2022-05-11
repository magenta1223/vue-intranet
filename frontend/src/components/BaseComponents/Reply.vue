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
            <v-col class = "btn-containter text-start">
                <v-btn
                class="ma-2"
                outlined
                color="indigo"
                @click="replyCreate()"
                >
                Reply  
                </v-btn>
                
            </v-col>
        </v-row>

        <v-row v-for="(reply, index) in repliesNowPage" :key="reply.id">
            <v-col>
                
                <v-card class = "elevation0" outlined>
                    <div class = "box">
                        <v-card-text
                        v-if="user_id == reply.author"
                        class="text-start">
                            {{reply.author}} &#183;
                            {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}} &#183;
                            <a @click="prepareUpdate(reply, index)">수정</a> &#183;
                            <a @click="deleteReply(reply, index)">삭제</a>
                        </v-card-text>
                        <v-card-text v-else class="text-start">
                            {{reply.author}} &#183;
                            {{parseDate(reply.create_date, "YYYY-MM-DD HH:mm", false)}}
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
                                @click="updateReply(reply, replyNow)"
                                >
                                Update  
                                </v-btn>
                            </v-row>                        
                        </v-container>
                        
                        <v-card-text v-else class="text-start">
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
import parseDate from "../../js_utils/date.js"
import axios from "axios";
import setToken from "../../js_utils/token.js"

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

        set_page : function(){
            this.page_length = parseInt((this.reply_set.length - 1) / 10) + 1 ;
        },

        paging : function(page){
            this.repliesNowPage = this.reply_set.slice( (page-1) * 10, page * 10)
        },

        replyCreate : function(){
            axios({
                method : "POST",
                url : url,
                headers : setToken(),
                params : {
                    "wrapper_id" : this.wrapper_id,
                    "reply" : this.reply,
                    "user_id" : localStorage.getItem('user')
                }
            })
            .then((response) => {
                this.reply = "";
                this.reply_set.push(response.data)
                }
            )
            
        },

        prepareUpdate : function(reply, index){
            if (this.updating_reply > -1){
                // 이전에 업데이트하고 있었던 reply의 update 취소
                this.repliesNowPage[this.updating_reply].update = false
            }
            // 현재 update하는 reply 정보
            this.updating_reply = index 
            reply.update = true
            this.replyNow = reply.content
            this.paging(this.page); //새로고침 해야 textfield가 나옴
        },

        updateReply : function(reply, replyNow){
            reply.content = replyNow;
            axios({
                method: "PUT",
                url : url + reply.id,
                headers : setToken(),
                params : {
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

        deleteReply : function(reply, index){
            axios({
                method: "DELETE",
                url : url + reply.id,
                headers : setToken(),
            })
            .then((response) => {
                // index 이용해서 reply 삭제하면 됨
                this.reply_set.splice(index, 1)
            })
            .catch(response => {
                console.log("Failed", response);
            });
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
                
        page : function(newParam, oldParam){
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
