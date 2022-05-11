import VueRouter from 'vue-router'

// my apps

import Login from '../components/Auth/Login.vue'
import Register from '../components/Auth/Register.vue'

// post
import PostList from '../components/Board/PostList.vue'
import PostCreate from '../components/Board/PostCreate.vue'
import PostRetrieval from '../components/Board/PostRetrieval.vue'

// calendar & events
import ToastCalendar from '../components/Calendar/Calendar.vue'

// profile
import Profile from '../components/Profile/Profile.vue'


// 중첩 라우팅
// https://jeonghwan-kim.github.io/2018/04/07/vue-router.html

const router = new VueRouter({
	mode:'history', //해쉬값 제거 방식
    routes: [

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
            path: '/post/:category_id', // dynamic routing https://whwl.tistory.com/39
            component: PostList, //  
            name : 'postlist'

        },
        {
            path: '/post/:category_id/create', 
            component: PostCreate, //  
            name : 'post_create'
        },
        {
            path: '/post_retrieval', 
            component: PostRetrieval, //  
            name : 'post_retrieval'
        },
        {
            path: '/calendar', 
            component: ToastCalendar, //  
            name : 'calendar'
        },
        {
            path: '/profile', 
            component: Profile, //  
            name : 'profile'
        },
    ]
});


// router.beforeEach(async(to, from, next) => {

//     // accesstoken을 가져왔는데 없고
//     // refreshtoken은 있음
//     // 갱신
//     if (VueCookies.get('token') === null && VueCookies.get('refresh_token') !== null){
//         await refreshToken()
//     }

//     // 몰라
//     if (to.matched.some(record => record.meta.unauthorized) || VueCookies.get('token')){
//         return next()
//     }

//     // 로그인
//     alert('login please')
//     return next('/login')
// })


export default router