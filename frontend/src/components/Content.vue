<template>
    <div>
        <v-container fluid>
            <v-layout column>
                <v-flex xs12>
                    <h3 class="subject">User CRUD</h3>
                </v-flex>
                <v-flex column>
                    <v-row>
                        <v-col cols="4" md="4">
                            <!-- 합이 12가 되면 전체 화면을 사용한다는 의미입니다. -->
                            <v-text-field
                                v-model="data.username"
                                :counter="15"
                                label="Username"
                                required
                            ></v-text-field>
                        </v-col>
                        <v-col cols="4" md="4">
                            <v-text-field v-model="data.age" label="Age" required></v-text-field>
                        </v-col>
                        <v-col cols="4" md="4">
                            <v-text-field
                                v-model="data.city"
                                :counter="15"
                                label="City"
                                required
                            ></v-text-field>
                        </v-col>
                    </v-row>
                    <!-- 수정하는 부분 start-->
                    <v-btn @click="sendForm" style="background: green">create</v-btn>
                    <v-btn @click="clearForm" style="background: red">clear</v-btn>
                </v-flex>
                <v-flex class="userList" column>
                    <v-card fluid>
                        <v-list-item v-for="(data, index) in propsdata" v-bind:key="index">
                            <v-list-item-content v-show="!data.is_hidden">
                                <v-list-item-title>이름 : {{ data.username }}</v-list-item-title>
                                <v-list-item-subtitle
                                    >나이 : {{ data.age }}세, 거주지:
                                    {{ data.city }}</v-list-item-subtitle
                                >
                            </v-list-item-content>
                            <v-form v-show="data.is_hidden">
                                <!-- is_hidden=true 가 되면 수정하는 form 등장 -->
                                <v-container>
                                    <v-row>
                                        <v-col cols="12" md="4">
                                            <v-text-field
                                                v-model="data.username"
                                                :counter="15"
                                                label="Username"
                                                required
                                            >
                                            </v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="4">
                                            <v-text-field v-model="data.age" label="Age" disabled>
                                            </v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="4">
                                            <v-text-field v-model="data.city" label="City" required>
                                            </v-text-field>
                                        </v-col>
                                        <v-col cols="12" md="4">
                                            <!-- Save 버튼은 Update 버튼을 클릭하면 볼 수 있고, Save 버튼 클릭 시 is_hidden=false 를 전달함 -->
                                            <v-btn
                                                class="ma-2"
                                                @click="
                                                    data.is_hidden = !data.is_hidden;
                                                    updateUser(data);
                                                "
                                                v-show="data.is_hidden"
                                                color="#4CAF50"
                                                >Save</v-btn
                                            >
                                            <!-- Delete 버튼은 Update 버튼을 클릭하면 볼 수 있고, Delete 버튼 클릭 시 선택 된 객체를 삭제함 -->
                                            <v-btn
                                                class="ma-2"
                                                @click="deleteUser(data.id)"
                                                color="#F44336"
                                                >Delete
                                            </v-btn>
                                        </v-col>
                                    </v-row>
                                </v-container>
                            </v-form>
                            <!-- Update 버튼 클릭 시 하나의 객체만 띄울 수 있는 메소드로 데이터 전달 -->
                            <v-btn
                                class="ma-2"
                                @click="
                                    data.is_hidden = !data.is_hidden;
                                    onlyUserListCard(data, propsdata);
                                "
                                v-show="!data.is_hidden"
                                color="#F9A825"
                                >Update</v-btn
                            >
                            <!-- 수정하는 부분 end-->
                            <v-btn class="ma-2" @click="deleteUser(data.id)" color="#F44336"
                                >Delete</v-btn
                            >
                        </v-list-item>
                    </v-card>
                </v-flex>
            </v-layout>
        </v-container>
    </div>
</template>

<script>
import axios from "axios";
let url = "http://127.0.0.1:8000/user/";

export default {
    data: () => {
        return {
            data: {
                username: "",
                age: "",
                city: "",
            },
        };
    },
    props: ["propsdata"],
    methods: {
        sendForm: function() {
            axios({
                method: "POST",
                url: url,
                data: this.data,
            })
                .then((response) => {
                    this.userList = response.data;
                    this.$emit('saved') // app으로 데이터를 보냄
                })
                .catch((error) => {
                    console.log("Failed to get userList", error.response);
                });
        },
        clearForm: function() {
            (this.data.username = ""), (this.data.age = ""), (this.data.city = "");
        },
        deleteUser: function(id) {
            axios({
                method: "DELETE",
                url: url + id, // localhost:8000/user/1 로 delete method
            })
                .then((response) => {
                    this.$emit("deleted"); // 상위 컴포넌트에 deleted 이벤트를 전송함
                    console.log("Success", response);
                })
                .catch((error) => {
                    console.log("Failed to get userList", error.response);
                });
        },
        // 추가되는 부분
        updateUser: function(data) {
            // 입력한 데이터를 PATCH로 업데이트 함
            axios({
                method: "PATCH",
                url: url + data.id + "/",
                data: data,
            })
                .then((response) => {
                    this.$emit("patched"); // 상위 컴포넌트에 patched 이벤트를 전송함
                    console.log("Success", response);
                })
                .catch((error) => {
                    console.log("Failed to patched userList", error.response);
                });
        },
        // 추가되는 부분
        onlyUserListCard: function(data, propsdata) {
            // 한개의 리스트만 보이도록 하는 함수
            for (var index in propsdata) {
                data.id != propsdata[index].id ? (propsdata[index].is_hidden = false) : "";
            }
        },
    },
};
</script>

<style>
.subject {
    color: blue;
    font-style: oblique;
    padding: 30px;
    text-align: center;
}
.userList {
    margin: 30px 0px 30px 0px;
}
</style>