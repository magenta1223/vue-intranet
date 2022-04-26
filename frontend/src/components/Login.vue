// 로그인이 되었는지 안되었는지 확인
// 로그인이 되어있다면 > main으로 넘어가면 되겠고
// 안되어 있다면 > 로그인 페이지로 넘어가면 됩니다


<template>
   <v-app>
      <v-main>
         <v-container fluid fill-height>
            <v-layout align-center justify-center>
               <v-flex>
                  <v-card class="elevation-12">
                     <v-toolbar dark color="primary">
                        <v-toolbar-title>
                            Login form
                        </v-toolbar-title>
                        <a id = "register" @click="Register" > or Register </a>

                     </v-toolbar>
                     <v-card-text>
                        <v-form>
                           <v-text-field
                                v-model="data.username"
                                name="username"
                                label="Email/ID"
                                type="text"
                           ></v-text-field>
                           <v-text-field
                                v-model="data.password"
                                id="password"
                                name="password"
                                label="Password"
                                type="password"
                           ></v-text-field>
                        </v-form>
                     </v-card-text>
                     <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="Login">Login</v-btn>
                     </v-card-actions>
                  </v-card>
               </v-flex>
            </v-layout>
         </v-container>
      </v-main>
   </v-app>
</template>

<script>
import axios from "axios";
let url = "http://127.0.0.1:8000/api/login";

export default {
    data: () => {
        return {
            data: {
                username: "",
                password : ""
            },        
        };
    },

   methods : {
       Login :function() {
            axios({
                method: "POST",
                url: url, // localhost:8000/user/1 로 delete method
                data: this.data,
            })
                .then((response) => {
                    console.log(response.data.user);

                    //this.$emit(); 상부 구조가 아니라 못보내는구나
                    localStorage.setItem('access_token', response.data.access_token);
                    localStorage.setItem('refresh_token', response.data.refresh_token);
                    localStorage.setItem('user', response.data.user.id);
                    // js redirect
                    // window.location.href = 'http://localhost:8080/';
                    
                    // vue
                    //this.$router.push({ name : 'home'})
                    this.$router.go(this.$router.currentRoute);
                })
                .catch((error) => {
                    console.log("Failed to get userList", error.response);
                });
        },
    Register :function() {
        this.$router.push({ name : 'register'})

            },

   }
};
</script>

<style>
#register {
    margin-left : auto ;
    color : white;
}


</style>
