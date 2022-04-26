import Vue from 'vue';
import App from './App.vue';
import axios from "axios";
import vuetify from './plugins/vuetify'
import VueRouter from 'vue-router'

import router from './router/router.js'
import setToken from './js_utils/token.js'

Vue.use(VueRouter);


let url = "http://localhost:8000/api/landing/"; // 장고 서버 주소


axios({
    method: "GET",
    url : url,
    headers : setToken(),
})
.then(function(response){
    console.log('success');
    let categories = response.data.categories
})
.catch(function(response){
    console.log(url);
    console.log('failed');
  console.log(response);
})



Vue.config.productionTip = false;


new Vue({
    router,
    vuetify,
    


  render: h => h(App),
}).$mount('#app')
