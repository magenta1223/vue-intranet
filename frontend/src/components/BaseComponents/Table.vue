<template>
    <v-container >
        <v-row justify="center">
            <v-col class ="text-start text-h2 active mb-2 justify-center">
                Hi
            </v-col>
            <v-col class = "btn-containter">
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
            </v-col>
        </v-row>
        <v-row>
            <v-col class="text-start">
                simple description of this board
            </v-col>
        </v-row>
                
            

        <v-row v-for="wrapper in page_item" :key="wrapper.id">
                
                <v-col class = "title" link @click="detail(wrapper.id)" v-ripple>
                    
                    <v-card-title class="text-start">
                        title : {{wrapper.title}}
                    </v-card-title>

                    <v-card-text class="text-start">
                        작성자 : {{wrapper.author}} 작성일자 : {{to_datetime(wrapper.create_date).format("YYYY-MM-DD HH:mm")}}
                    </v-card-text>
                    <v-divider></v-divider>
                </v-col>
            
        </v-row>

        
            <v-row justify="center">
                <v-col cols="8" class="max-width">
                    <v-pagination
                    v-model="page"
                    class="my-4"
                    :length="page_length"
                    ></v-pagination>
                </v-col>
            </v-row>
        



            
    </v-container>
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
            detail_route : ""
            }
        },
    props: ["propsdata", "content_type", "category_id"],

    methods : {
        detail : function(wrapper_id) {
            
            if (this.content_type == 'post'){
                this.route_name = "post_retrieval"
            } else {
                this.route_name = "post_retrieval"
            }
            
            this.$router.push({
                name : this.route_name, // wrapper type에 따라 바뀌게 수정
                params : {
                    wrapper_id : wrapper_id,
                    content_type : this.content_type,
                    category_id : this.category_id   
                }
                });
        },

        create : function(){

            if (this.content_type === "post"){
                console.log(this.category_id);
                this.$router.push({
                    name : 'post_create',
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