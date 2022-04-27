<template>
    <div class = "posting-container">
        <v-sheet>
            <v-layout>
                <v-flex>
                    <v-list-item class ="text-h2 active mb-2">
                        Hi
                    </v-list-item>
                    <v-list-item class ="text-h6 active mb-2">
                        simple description of this board
                    </v-list-item>
                </v-flex>
                <v-flex class = "btn-containter" xl-4>
                    <div class="text-center">
                        <v-btn
                        class="ma-2"
                        outlined
                        color="indigo"
                        @click="create()"
                        >
                        Create!  
                        </v-btn>
                    </div>
                </v-flex>
            </v-layout>
        </v-sheet>
            
        <v-sheet v-for="wrapper in page_item" :key="wrapper.id">
            <v-list-item link @click="detail(wrapper.id)">
                <v-flex class = "title" >
                    <v-card-title>
                        title : {{wrapper.title}}
                    </v-card-title>

                    <v-card-text class="d-flex justify-space-between text-caption">
                        작성자 : {{wrapper.author}} 작성일자 : {{to_datetime(wrapper.create_date).format("YYYY-MM-DD HH:mm")}}
                    </v-card-text>
                <v-divider></v-divider>
                </v-flex>
             </v-list-item>
        </v-sheet>

    <v-container>
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



            
    </div>
</template>

<script>
import dayjs from "dayjs"

export default {
    
    data : () => {
        return {

            page: 1,

            page_length : 0,

            page_item : [],
            user : localStorage.getItem('user'),
            }
        },
    props: ["propsdata", "content_type", "category_id"],

    methods : {
        detail : function(wrapper_id) {            
            this.$router.push({
                name : "detail",
                params : {
                    wrapper_id : wrapper_id,
                    content_type : this.content_type   
                }
                });
        },

        create : function(){

            if (this.content_type === "post"){
                console.log(this.category_id);
                this.$router.push({
                    name : 'board_create',
                    params : {
                        wrapper_id : -1,
                        category_id : this.category_id,
                        update : false,
                    }
                })
            }
        },

        to_datetime : function(time){
            return dayjs(time)
        },

        set_page : function(){
            this.page_length = parseInt(this.propsdata.length / 10) + 1 ;
        },
        paging : function(page){
            this.page_item = this.propsdata.slice( (page-1) * 10, page * 10)
        }
    },
    
    watch: { 
        // () => 이런거 쓰면 개박살남
        // 시부레..
        'propsdata': function(newParam, oldParam) {
            this.set_page();
            this.paging(1)
        },
        'page': function(newParam, oldParam) {
            // page에 따라서 propsdata를 수정하면 됨
            this.paging(newParam)
        },
    },

    }


</script>

<style scoped>
    .btn-containter{
        margin-top: 0;
        align-content: center;
    }

    .btn{
        margin-left: auto;
    }
.posting-container{
    margin-bottom: auto;
}


</style>