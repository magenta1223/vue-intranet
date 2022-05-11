<template>
    <div>
        <!-- 라우팅 링크 -->
        <!-- rounter link를 죽 모아서 사이드바로 -->
        <div id="container">
            <!-- register 클릭 시 보여줄 수 있게 여기에서 작업하자
            v-else 아래에 하나 더 넣으면 되겠죠~ -->
            <div v-if="isLogin">
                <SideBar v-bind:login="this.isLogin" v-bind:categories="this.categories"/>
            </div>
            <div v-else>
                <Login/>
            </div> 
        </div>
    </div>
</template>

<script>
import Login from "./components/Auth/Login.vue"
import SideBar from './components/Main/SideBar.vue'
import axios from "axios";
import setToken from "./js_utils/token.js"
import router from './router/router.js'


let url = "http://localhost:8000/api/landing/"; // 장고 서버 주소


export default {



    data: function () {
        return {
        isLogin : false,
        categories: [
            {names: 'login', router: '/login', id: 1},
          ]
        
        }
    },

    methods: {
        Logout : () => {
            localStorage.removeItem('access_token');
            location.reload();
        },


    },
    created : function(){
        // 로컬스토리지에 jwt 이 존재하는지에 따라 로그인 여부 판단하기
        const token = localStorage.getItem('access_token')
        if(token){
            this.isLogin = true
        }
    }, // 얘도 token.js로 빼자

    mounted() {

        axios({
            method: "GET",
            url : url,
            headers : setToken(),
        })
        .then( (response) => {
            this.categories = response.data.categories;
            
        })
        .catch( (response) => {
            console.log("개같이멸망");
        })
    },


    components : {
        Login,
        SideBar
    }


}
</script>

<style></style>