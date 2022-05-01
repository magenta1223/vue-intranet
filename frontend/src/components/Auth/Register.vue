// App.vue 수정

<template>
    <div>
        <v-container fluid>
            <v-layout column>
                <v-flex xs12>
                    <h3 class="subject">User CRUD</h3>
                </v-flex>
                <v-flex column>
                    <v-row>
                        <v-col cols="3" md="3">
                            <!-- 합이 12가 되면 전체 화면을 사용한다는 의미입니다. -->
                            <v-text-field
                                v-model="data.username"
                                label="Username"
                                required
                            ></v-text-field>
                        </v-col>
                        <v-col cols="3" md="3">
                            <v-text-field
                                v-model="data.age"
                                label="Age"
                                required></v-text-field>
                        </v-col>
                        <v-col cols="3" md="3">
                            <v-text-field
                                v-model="data.city"
                                label="City"
                                required
                            ></v-text-field>
                        </v-col>
                         <v-col cols="3" md="3">
                            <v-text-field
                                v-model="data.password"
                                label="password"
                                required
                            ></v-text-field>
                        </v-col>
 
                    </v-row>
                    <!-- 수정하는 부분 start-->
                    <v-btn @click="sendForm" style="background: green">create</v-btn>
                </v-flex>
                
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import axios from "axios";

let url = "http://127.0.0.1:8000/api/register";  // 장고 drf 서버 주소


export default {
    data: () => {
        return {
            data: {
                username: "",
                age: "",
                city: "",
                password : ""
            },
        
        };
    },
    components: {
    },
    methods: {
        sendForm: function() {
            console.log(this.data);
            axios({
                method: "POST",
                url: url,
                data: this.data,
            })
                .then((response) => {
                    console.log('회원가입');
                    window.location.href = 'http://localhost:8080/';

                })
                .catch((error) => {
                    console.log("Failed to get userList", error.response);
                });
        },
    }


    
};
</script>

<style></style>