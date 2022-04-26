<template>
    <!-- https://fkkmemi.github.io/nemv/nemv-082-dashboard-layout/ -->
    <v-app>
        <v-layout fluid>
            <v-navigation-drawer class= "sidebar" v-model="drawer" :mini-variant.sync="mini" app permanent>
                <v-list-item class="px-2">
                    <v-list-item-avatar>
                    <v-img src="https://randomuser.me/api/portraits/men/85.jpg"></v-img>
                    </v-list-item-avatar>

                    <v-list-item-title>
                        John Leider
                    </v-list-item-title>
                    <v-btn icon @click.stop="mini = !mini">
                        <v-icon>mdi-chevron-left</v-icon>
                    </v-btn>
                </v-list-item>
                <v-list dense>
                    <v-list-item link>
                        <v-list-item-content @click="Logout">
                            Logout
                        </v-list-item-content>
                    </v-list-item>
                </v-list>
                <v-divider></v-divider>

                <v-list dense>
                    <v-list-item link>
                        <router-link to="/">home </router-link>
                    </v-list-item>
                    <v-list-item v-for="item in categories" :key="item.id" link>
                        <v-list-item-content>
                            <router-link :to="{ name :'board', params: { type : 'post', category_id : item.id }}"> {{item.name}} </router-link>
                        </v-list-item-content>
                    </v-list-item>
                    
                </v-list>
            </v-navigation-drawer>
        </v-layout>



        <v-layout>
            <router-view class = "container"></router-view> 
        </v-layout>
    </v-app>
</template>




<script>
import router from '../router/router.js'

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
        }
        },
    props: ["login", "categories"],

    methods : {
        Logout : () => {
            localStorage.removeItem('access_token');
            location.reload();
        },
    }
}
</script>

<style scoped>
    .sidebar{
        max-width: 20%!important;
    }

    .container{
        margin-left: 56px!important;
    }

</style>