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
                        <v-col>
                            <v-text-field
                                v-model="data.username"
                                label="ID"
                                required
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="data.password"
                                label="비밀번호를 입력하세요"
                                required></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="data.password2"
                                label="비밀번호 확인"
                                required></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col>
                            <v-text-field
                                v-model="data.name"
                                label="이름"
                                required></v-text-field>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-menu
                        v-model="picker"
                        :close-on-content-click="closeByclick"
                        :nudge-right="40"
                        transition="scale-transition"
                        offset-y
                        min-width="auto"
                        >
                            <template v-slot:activator="{ on, attrs }">
                                <v-text-field
                                    v-model="data.date"
                                    label="생년월일"
                                    prepend-icon="mdi-calendar"
                                    readonly
                                    v-bind="attrs"
                                    v-on="on"
                                    @click="closeByclick = false"
                                ></v-text-field>
                            </template>
                            <v-date-picker
                            v-model="data.date"
                            @input="pickerOff(picker)"
                            ></v-date-picker>
                        </v-menu>
                    </v-row>

 
                    <!-- 수정하는 부분 start-->
                    <v-btn @click="createUser" style="background: green">create</v-btn>
                </v-flex>
                
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import axios from "axios";
import setToken from "../../js_utils/token.js"

let url = "http://127.0.0.1:8000/api/register";  // 장고 drf 서버 주소


export default {
    data: () => {
        return {
            data : {            
            username: "",
            password: "",
            password2: "",
            name : "",
            date : "",
            dateOfBirth : "",
            },
            closeByclick : false,
            picker : false
        };
    },
    components: {
    },
    methods: {

        createUser: function() {
            axios({
                method: "POST",
                url: url,
                headers : setToken(),
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
        pickerOff : function(controller){
            console.log('modal off')
            controller = false  
            this.closeByclick = true  
            this.data.dateOfBirth = new Date(this.data.date).toISOString()

        },
    }


    
};
</script>

<style></style>