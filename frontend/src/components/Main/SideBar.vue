<template>
    <!-- https://fkkmemi.github.io/nemv/nemv-082-dashboard-layout/ -->
    <v-app>
        <v-row>
            <v-col  cols="2" sm="2" md="2" lg="3" xl="3">
                <v-navigation-drawer class= "sidebar" v-model="drawer" app permanent expand-on-hover :mini-variant.sync="mini">
                    <v-list dense> 
                        <v-list-item class="px-2">
                            <v-list-item-avatar>
                                <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
                            </v-list-item-avatar>

                            <v-list-item-title>
                                {{username}}
                            </v-list-item-title>
                            <v-btn icon @click.stop="mini = !mini">
                                <v-icon>mdi-chevron-left</v-icon>
                            </v-btn>
                        </v-list-item>
                        <v-list-item>
                            <router-link :to="{name : 'profile'}"> Profile </router-link>
                        </v-list-item>
                        <v-list-item link>
                            <v-list-item-content @click="Logout">
                                Logout
                            </v-list-item-content>
                        </v-list-item>
                        <v-divider></v-divider>

                        <v-list-item link>
                            <router-link to="/">home </router-link>
                        </v-list-item>
                        <v-list-item v-for="item in categories" :key="item.id" link>
                            <v-list-item-content>
                                <router-link :to="{ name :'postlist', params: { type : 'post', category_id : item.id }}"> {{item.name}} </router-link>
                            </v-list-item-content>
                        </v-list-item>
                        <v-list-item link>
                            <router-link :to="{name : 'calendar'}">calendar </router-link>
                        </v-list-item>
                        
                    </v-list>
                </v-navigation-drawer>
            </v-col>
            <v-col   align="center">
                <router-view class = "container"></router-view> 
            </v-col>
            <v-col cols="1" sm="2" md="2" lg="3" xl="3"></v-col>
        </v-row>
        


        <!-- <v-row>
            <router-view class = "container"></router-view> 
        </v-row> -->
    </v-app>
</template>




<script>
import axios from 'axios';
import setToken from "../../js_utils/token.js"

let url = 'http://localhost:8000/user/'

export default {
    data () {
        return {
            drawer: true,
            items: [
            { title: 'Home', icon: 'mdi-home-city' },
            { title: 'My Account', icon: 'mdi-account' },
            { title: 'Users', icon: 'mdi-account-group-outline' },
            ],
            mini: true,
            username : ""
        }
        },
    props: ["login", "categories"],

    methods : {
        Logout : function() {
            localStorage.removeItem('access_token');
            location.reload();
        },

    },

    mounted() {
        let user = localStorage.getItem('user')

        axios({
            method : "GET",
            url : url + user,
            headers: setToken(),
            params : {
                user_id : user
            }
        }).then((response) => {
            this.username = response.data.name
            
        }).catch((response) => {
            console.log("Failed", response)
        })
    }
}
</script>

<style scoped>


</style>