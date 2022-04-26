// App.vue 수정

<template>
    <div>
        <VHeader/>
        <VContent v-bind:propsdata="userList"/>
        <VFooter/>
    </div>
</template>

<script>
import axios from "axios";

import VHeader from "./components/Header.vue";
import VFooter from "./components/Footer.vue";
import VContent from "./components/Content.vue";



export default {
    data: () => {
        return {
        userList: []
        };
    },
    components: {
        VHeader,
        VContent,
        VFooter,
    },
    mounted() { // DOM 객체가 생성된 후 DRF server 에서 데이터를(userList) 가져와 저장
    },

    methods: {  // CRUD 로직 
        setToken : function () { // header 내용에 토큰 붙여주기
            const token = localStorage.getItem('access_token')
            const config = {
                username : "test1234@test.com",
                password : "thwn1256"
            }
            return config
            },

        
    }
};
</script>

<style></style>