import VueRouter from 'vue-router'

// my apps

import Home from '../App_copy.vue'
import Login from '../components/Login.vue'
import Register from '../components/Register.vue'
import Detail from '../components/PostDetail.vue'
import Board from '../components/Board.vue'
import BoardCreate from '../components/BoardCreate.vue'


// 중첩 라우팅
// https://jeonghwan-kim.github.io/2018/04/07/vue-router.html

const router = new VueRouter({
	mode:'history', //해쉬값 제거 방식
    routes: [
        {
            path: '/', 
            component: Home, //  
            name : 'home'
        },
        {
            path: '/login', 
            component: Login, //  
            name : 'login'

        },
        {
            path: '/register', 
            component: Register, //  
            name : 'register'

        },
        {
            path: '/board/:category_id', // dynamic routing https://whwl.tistory.com/39
            component: Board, //  
            name : 'board'

        },
        {
            path: '/detail', 
            component: Detail, //  
            name : 'detail'
        },
        {
            path: '/board/:category_id/create', 
            component: BoardCreate, //  
            name : 'board_create'
        }
    ]
});


export default router