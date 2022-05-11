<template>
    <v-container>
        <v-row justify="center">
            <v-col class ="text-start text-h2 active mb-2 justify-center">
                Profile 
            </v-col>
        </v-row>

        <v-row>
            <v-col class="text-start">
                <v-card class = "elevation-0" >
                    <v-text-field
                    v-model="user.name"
                    label = "이름"
                    :readonly="readonly">
                    </v-text-field>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <datePicker v-model="user.dateOfBirth" :readonly="readonly"/>
        </v-row>
        <v-row>
            <v-col class="text-start">
                <v-card class = "elevation-0" >
                    <v-text-field
                    v-model="user.password"
                    label = "비밀번호"
                    :readonly="readonly">
                    </v-text-field>
                </v-card>
            </v-col>
        </v-row>
        <v-row>
            <v-col class="text-start">
                <v-card class = "elevation-0" >
                    <v-text-field
                    v-model="user.vacation"
                    label = "잔여 휴가 일수"
                    readonly>
                    </v-text-field>
                </v-card>
            </v-col>
        </v-row>

        <v-row>
            <v-col v-if="readonly">
                <v-btn @click="activateEdit()">
                    Edit
                </v-btn>
            </v-col>
            <v-col v-else>
                <v-btn @click="save()">
                    Save
                </v-btn>
            </v-col>
        </v-row>




    </v-container>
</template>

<script>
import axios from "axios";
import setToken from "../../js_utils/token.js"
import datePicker from "../BaseComponents/DatePicker.vue"

let url = 'http://localhost:8000/user/'

export default {
    data() {
        return {
            user : {},
            closeByclick : false,
            readonly : true
            

        }
    },

    mounted() {
        // user 정보를 가져오면 됨
        let user = localStorage.getItem('user')

        axios({
            method : "GET",
            url : url + user,
            headers: setToken(),
            params : {
                user_id : user
            }
        }).then((response) => {
            console.log(response.data)
            this.user = response.data
            this.user.dateOfBirth = this.user.dateOfBirth.substr(0,10)
            this.user.password = ""
        }).catch((response) => {
            console.log("Failed", response)
        })

        

    },

    components :{
        datePicker
    },

    methods : {
        activateEdit : function(){
            this.readonly = false
        },

        save : function(){

            axios({
                method : 'PUT',
                url : url + localStorage.getItem('user') + '/',
                headers : setToken(),
                params : {
                    name : this.user.name,
                    dateOfBirth : new Date(this.user.dateOfBirth).toISOString(),
                    password : this.user.password
                }
            }).then((response) => {
            }).catch((response) => {
            })
        }

    },
    
    watch : {

    },
    computed : {

    }



}
</script>


