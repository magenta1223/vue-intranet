<template v-slot:default>
    <!-- https://velog.io/@jsg3121/%ED%95%9C%EB%8B%AC%EC%97%90-%ED%95%98%EB%82%98%EC%94%A9-CRUD%EA%B2%8C%EC%8B%9C%ED%8C%90-4 -->
    <Table v-bind:propsdata="this.items" v-bind:content_type="this.content_type" v-bind:category_id="this.category_id"/>
</template>

<script>
import axios from "axios";
import Table from "../BaseComponents/Table.vue"
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/wrapper/";  // 장고 drf 서버 주소


export default {
    
    data : () => {
        return {
            items : [{
                id : 0
            }],
            content_type : "post",
            category_id : -1,
            }
        },

    components : {
        Table
    },
    
    // param이 바뀌어도 갱신이 되지 않음
    // board는 이미 mount가 끝났기 때문
    // 그래서 mounted를 call하지 않음
    // mounted를 method화 하고, param을 watch하면서 변경될때마다 call하면 됨
    methods: {
        fetchData : function(params) {
            this.content_type = "post";
            this.category_id = params.category_id;

            axios({
                method: "GET",
                url : url,
                headers : setToken(),
                params : {
                    // 어차피 board 전용임
                    "content_type" : "post", //this.content_type, // 이게 왜 없지? 
                    "category_id" : this.category_id
                }
            })
            .then((response) => {
                console.log(response.data)
                this.items = response.data;
            })
            .catch(response => {
                console.log("Failed", response);
            });
        }
    },



    watch: { 
        // () => 이런거 쓰면 개박살남
        // 시부레..
        '$route.params': function(newParam, oldParam) {
            if (newParam.category_id != oldParam.category_id){
                this.fetchData(newParam)
            }
        }
    },

    mounted() {
        console.log(this);
        this.fetchData(this.$route.params)
    }

    }


</script>