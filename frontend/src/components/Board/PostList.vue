<template v-slot:default>
    <!-- https://velog.io/@
    sg3121/%ED%95%9C%EB%8B%AC%EC%97%90-%ED%95%98%EB%82%98%EC%94%A9-CRUD%EA%B2%8C%EC%8B%9C%ED%8C%90-4 -->
    <Table :items="items" :content_type="content_type" :category_id="category_id"/>
</template>

<script>
import axios from "axios";
import Table from "../BaseComponents/Table.vue"
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/wrapper/";  // 장고 drf 서버 주소


export default {
    
    data : () => {
        return {
            items : [],
            content_type : "post",
            category_id : -1,
            }
        },

    components : {
        Table
    },
    
    methods: {
        fetchData : function(params) {
            this.content_type = "post";
            this.category_id = params.category_id;

            axios({
                method: "GET",
                url : url,
                headers : setToken(),
                params : {
                    "content_type" : "post",
                    "category_id" : this.category_id
                }
            })
            .then((response) => {
                this.items = response.data;
            })
            .catch(response => {
                console.log("Failed", response);
            });
        }
    },

    watch: { 
        '$route.params': function(newParam, oldParam) {
            if (newParam.category_id != oldParam.category_id){
                this.fetchData(newParam)
            }
        }
    },

    mounted() {
        this.fetchData(this.$route.params)
    }

    }


</script>